from abc import ABC, abstractmethod
from ..components.server import Server
from ..components.flow import Flow

class AdmissionPolicy(ABC):
    """Abstract base class for admission control policies."""
    
    @abstractmethod
    def decide(self, flow: Flow, server: Server) -> bool:
        """
        Decide whether to admit a flow to a specific server.
        Returns True if admitted, False otherwise.
        """
        pass
