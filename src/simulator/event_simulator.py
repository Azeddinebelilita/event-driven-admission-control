import heapq
from typing import List, Dict, Any, Optional
from ..components.area import Area
from ..components.server import Server
from ..components.flow import Flow
from ..components.load_balancer import LoadBalancer
from ..policies.admission_policy import AdmissionPolicy
from ..utils.statistics import Statistics
from .event import Event

class EventDrivenSimulator:
    """Main simulation engine."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_time = 0.0
        self.event_queue = []
        self.stats = Statistics()
        
        # Initialize components
        self._init_areas()
        self._init_servers()
        self._init_policy()
        
        self.load_balancer = LoadBalancer(self.servers, strategy='random')

    def _init_areas(self):
        self.areas: List[Area] = []
        conf = self.config['areas']
        fc_conf = self.config['flow_classes']
        
        for i in range(conf['M']):
            area = Area(i, fc_conf['J'])
            # Pass list of rates directly from config
            area.configure_traffic(
                fc_conf['arrival_rates'],
                fc_conf['service_rates'],
                fc_conf['bitrates']
            )
            self.areas.append(area)

    def _init_servers(self):
        self.servers: List[Server] = []
        s_conf = self.config['servers']
        fc_conf = self.config['flow_classes']
        
        for i in range(s_conf['N']):
            server = Server(
                i, 
                s_conf['access_bandwidth'][i],
                fc_conf['max_flows_per_server'][i]
            )
            self.servers.append(server)

    def _init_policy(self):
        from ..policies.simple_heuristic import SimpleHeuristicPolicy
        p_type = self.config['admission_policy']['type']
        if p_type == 'simple_heuristic':
            self.policy = SimpleHeuristicPolicy()
        else:
             # Default
            self.policy = SimpleHeuristicPolicy()

    def schedule_event(self, time: float, event_type: str, data: Any):
        event = Event(time, event_type, data)
        heapq.heappush(self.event_queue, event)

    def run(self) -> Statistics:
        """Execute the simulation."""
        
        # Schedule initial arrivals for each area and class
        for area in self.areas:
            for j in range(area.num_classes):
                t = area.generate_inter_arrival(j)
                if t < self.config['simulation']['duration']:
                    self.schedule_event(t, 'ARRIVAL', {
                        'area_id': area.area_id, 
                        'class_id': j
                    })

        # Main Loop
        while self.event_queue:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            
            if self.current_time > self.config['simulation']['duration']:
                break
                
            if event.event_type == 'ARRIVAL':
                self._handle_arrival(event.data)
            elif event.event_type == 'DEPARTURE':
                self._handle_departure(event.data)
                
        return self.stats

    def _handle_arrival(self, data: dict):
        area_id = data['area_id']
        class_id = data['class_id']
        area = self.areas[area_id]
        
        # Record arrival
        self.stats.record_arrival(class_id)
        
        # Create Flow
        duration = area.generate_duration(class_id)
        bitrate = area.bitrates[class_id]
        
        # NOTE: Flow ID logic is simplified here; stats tracks counts
        flow = Flow(
            flow_id=self.stats.total_arrivals,
            flow_class=class_id,
            source_area=area_id,
            bitrate=bitrate,
            duration=duration,
            arrival_time=self.current_time
        )
        
        # Schedule next arrival for this area/class
        next_time = self.current_time + area.generate_inter_arrival(class_id)
        self.schedule_event(next_time, 'ARRIVAL', {'area_id': area_id, 'class_id': class_id})
        
        # Routing
        target_server = self.load_balancer.select_server(class_id)
        
        if target_server and self.policy.decide(flow, target_server):
            target_server.admit_flow(flow)
            self.stats.record_admission(class_id, target_server.server_id)
            self.stats.record_server_state(
                self.current_time, 
                target_server.server_id, 
                len(target_server.active_flows),
                target_server.current_bandwidth_usage
            )
            
            # Schedule Departure
            depart_time = self.current_time + flow.duration
            self.schedule_event(depart_time, 'DEPARTURE', {'flow': flow, 'server': target_server})
        else:
            self.stats.record_rejection(class_id)

    def _handle_departure(self, data: dict):
        flow = data['flow']
        server = data['server']
        server.release_flow(flow)
        self.stats.record_server_state(
            self.current_time, 
            server.server_id, 
            len(server.active_flows),
            server.current_bandwidth_usage
        )
