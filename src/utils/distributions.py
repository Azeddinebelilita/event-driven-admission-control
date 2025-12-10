import numpy as np
from typing import Optional

class Distribution:
    """Base class for probability distributions."""
    def sample(self) -> float:
        raise NotImplementedError

class Exponential(Distribution):
    """Exponential distribution generator."""
    def __init__(self, rate: float, seed: Optional[int] = None):
        self.rate = rate
        self.rng = np.random.default_rng(seed)

    def sample(self) -> float:
        return self.rng.exponential(scale=1.0/self.rate)

class Poisson(Distribution):
    """Poisson distribution generator."""
    def __init__(self, lam: float, seed: Optional[int] = None):
        self.lam = lam
        self.rng = np.random.default_rng(seed)

    def sample(self) -> float:
        return float(self.rng.poisson(lam=self.lam))

class Constant(Distribution):
    """Constant value generator for testing."""
    def __init__(self, value: float):
        self.value = value

    def sample(self) -> float:
        return self.value
