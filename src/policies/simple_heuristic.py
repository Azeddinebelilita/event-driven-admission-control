from .admission_policy import AdmissionPolicy
from ..components.server import Server
from ..components.flow import Flow

class SimpleHeuristicPolicy(AdmissionPolicy):
    """
    Admit flows if the server has capacity.
    Can be extended with more complex utility thresholds.
    """
    def __init__(self, utility_threshold: float = 0.0):
        self.utility_threshold = utility_threshold

    def decide(self, flow: Flow, server: Server) -> bool:
        # Check hard constraints first
        if not server.has_capacity(flow):
            return False
            
        # Here you could add logic based on utility
        # For now, we accept if capacity exists
        return True
