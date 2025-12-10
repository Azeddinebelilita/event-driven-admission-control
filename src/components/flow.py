from dataclasses import dataclass
from typing import Optional

@dataclass
class Flow:
    """Represents a single application flow."""
    flow_id: int
    flow_class: int
    source_area: int
    bitrate: float
    duration: float
    arrival_time: float
    server_id: Optional[int] = None
    
    def __repr__(self):
        return (f"Flow(id={self.flow_id}, class={self.flow_class}, "
                f"from=Area{self.source_area}, t={self.arrival_time:.2f})")
