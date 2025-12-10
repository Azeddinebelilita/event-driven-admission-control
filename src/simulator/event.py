from dataclasses import dataclass, field
from typing import Any, Literal
from .event_simulator import *

@dataclass(order=True)
class Event:
    """Simulation event ordered by timestamp."""
    time: float
    event_type: Literal['ARRIVAL', 'DEPARTURE'] = field(compare=False)
    data: Any = field(compare=False)
