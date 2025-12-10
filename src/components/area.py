from typing import List
from ..utils.distributions import Distribution, Poisson, Exponential

class Area:
    """Geographic area generating traffic flows."""
    def __init__(self, area_id: int, num_classes: int):
        self.area_id = area_id
        self.num_classes = num_classes
        self.arrival_generators: List[Distribution] = []
        self.duration_generators: List[Distribution] = []
        self.bitrates: List[float] = []

    def configure_traffic(self, arrival_rates: List[float], service_rates: List[float], bitrates: List[float]):
        """Setup stochastic processes for traffic generation."""
        self.bitrates = bitrates
        for lam in arrival_rates:
             self.arrival_generators.append(Exponential(rate=lam)) # Inter-arrival time is Exp(lambda)
        
        for mu in service_rates:
             self.duration_generators.append(Exponential(rate=mu)) # Duration is Exp(mu)

    def generate_inter_arrival(self, flow_class: int) -> float:
        return self.arrival_generators[flow_class].sample()

    def generate_duration(self, flow_class: int) -> float:
        return self.duration_generators[flow_class].sample()
        
    def get_bitrate(self, flow_class: int) -> float:
        return self.bitrates[flow_class]
