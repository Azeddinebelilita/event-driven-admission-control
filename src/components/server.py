from typing import List, Dict
from .flow import Flow

class Server:
    """Models an edge server with compute and bandwidth constraints."""
    def __init__(self, server_id: int, access_bandwidth: float, max_flows_per_class: List[int]):
        self.server_id = server_id
        self.total_bandwidth = access_bandwidth
        self.max_flows = max_flows_per_class  # K^i_j
        
        # State
        self.active_flows: List[Flow] = []
        self.current_bandwidth_usage = 0.0
        self.flows_per_class: Dict[int, int] = {j: 0 for j in range(len(max_flows_per_class))}

    def has_capacity(self, flow: Flow) -> bool:
        """Check if server has resources to admit the flow."""
        # check bandwidth
        if self.current_bandwidth_usage + flow.bitrate > self.total_bandwidth:
            return False
            
        # check compute capacity for specific class
        class_idx = flow.flow_class
        if class_idx < 0 or class_idx >= len(self.max_flows):
             # safe guard
             return False
        
        if self.flows_per_class[class_idx] >= self.max_flows[class_idx]:
            return False
            
        return True

    def admit_flow(self, flow: Flow):
        """Register a flow as active."""
        self.active_flows.append(flow)
        self.current_bandwidth_usage += flow.bitrate
        self.flows_per_class[flow.flow_class] += 1
        flow.server_id = self.server_id

    def release_flow(self, flow: Flow):
        """Remove a flow upon completion."""
        if flow in self.active_flows:
            self.active_flows.remove(flow)
            self.current_bandwidth_usage -= flow.bitrate
            self.flows_per_class[flow.flow_class] -= 1
            if self.current_bandwidth_usage < 0: # minimal floating point correction
                self.current_bandwidth_usage = 0.0

    def get_utilization(self) -> float:
        """Return fractional bandwidth utilization."""
        if self.total_bandwidth == 0:
            return 0.0
        return self.current_bandwidth_usage / self.total_bandwidth
