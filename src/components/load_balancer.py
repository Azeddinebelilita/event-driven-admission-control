import random
from typing import List, Optional
from .server import Server

class LoadBalancer:
    """Routes incoming flows to servers."""
    def __init__(self, servers: List[Server], strategy: str = 'random'):
        self.servers = servers
        self.strategy = strategy

    def select_server(self, flow_class: int) -> Optional[Server]:
        """Select a target server based on strategy."""
        candidates = self.servers
        
        if not candidates:
            return None

        if self.strategy == 'random':
            return random.choice(candidates)
            
        elif self.strategy == 'round_robin':
             # Simplified stateless round robin for demo, 
             # in a real persistent object we would keep index state
             # implementing random for now as placeholder for full logic
            return random.choice(candidates) 

        elif self.strategy == 'least_loaded':
            # Select server with lowest bandwidth utilization
            return min(candidates, key=lambda s: s.get_utilization())

        return random.choice(candidates)
