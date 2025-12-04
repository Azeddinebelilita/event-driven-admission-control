# Event-Driven Simulation of Admission Control to Multiple Servers

A parametric event-driven simulator for flow admission control in edge computing systems, based on the research paper "Optimal Flow Admission Control in Edge Computing via Safe Reinforcement Learning" by Fox et al.

## Overview

This simulator models a multi-server edge computing environment where:
- Multiple geographic **areas** (M) generate application flows
- Multiple **servers** (N) host applications with limited capacity
- An **admission control** policy decides which flows to admit based on resource constraints and utility functions
- Different **flow classes** (J) have varying characteristics (arrival rates, durations, bitrates)

## System Components

### 1. Area Traffic Generator
The main event-driven simulation engine that generates flow arrivals using:
- Poisson process (exponential inter-arrival times) per area and class
- Exponential flow durations
- Configurable flow characteristics (class, bitrate, source area)

### 2. Area Load Balancer
Routes incoming flows from areas to target servers using various strategies:
- Random routing
- Round-robin
- Least-loaded server selection
- Custom probability distributions

### 3. Server
Models edge servers with two key resource constraints:
- **Computing capacity**: Maximum concurrent flows per class (K^i_j)
- **Access bandwidth**: Total bandwidth available (θ^i)

### 4. Admission Control
Pluggable policy architecture supporting:
- Simple heuristic-based policies (threshold-based)
- Custom admission logic
- Future integration with RL-based optimal policies

### 5. Application
Processes admitted flows with configurable utility functions:
- Linear utility: constant weight per class
- Load-dependent utility: decreases with server load
- Custom utility functions

## Project Structure

```
event-driven-admission-control/
├── src/
│   ├── simulator/
│   │   ├── event_simulator.py    # Main simulation engine
│   │   └── event.py               # Event class definition
│   ├── components/
│   │   ├── area.py                # Area with traffic generator
│   │   ├── server.py              # Server with capacity management
│   │   ├── flow.py                # Flow data class
│   │   └── load_balancer.py       # Load balancing strategies
│   ├── policies/
│   │   ├── admission_policy.py    # Base policy interface
│   │   └── simple_heuristic.py    # Simple threshold-based policy
│   └── utils/
│       ├── distributions.py       # Random number generators
│       └── statistics.py          # Metrics collection
├── config/
│   └── simulation_config.yaml     # Simulation parameters
├── tests/
│   ├── test_simulator.py          # Simulator tests
│   └── test_components.py         # Component tests
├── examples/
│   └── basic_simulation.py        # Example usage
├── docs/
│   ├── DESIGN.md                  # Architecture details
│   └── USAGE.md                   # Usage guide
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Azeddinebelilita/event-driven-admission-control.git
cd event-driven-admission-control

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from src.simulator.event_simulator import EventDrivenSimulator
from src.utils.statistics import Statistics
import yaml

# Load configuration
with open('config/simulation_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create and run simulator
simulator = EventDrivenSimulator(config)
stats = simulator.run()

# View results
stats.print_summary()
stats.export_to_csv('results.csv')
```

## Configuration

Edit `config/simulation_config.yaml` to customize:

```yaml
simulation:
  duration: 1000.0        # Simulation time
  random_seed: 42         # For reproducibility

areas:
  M: 4                    # Number of areas

servers:
  N: 3                    # Number of servers
  access_bandwidth: [100, 150, 120]  # θ^i for each server

flow_classes:
  J: 3                    # Number of classes
  arrival_rates: [2.0, 1.5, 1.0]     # Q_j (Poisson)
  service_rates: [0.5, 0.3, 0.4]     # μ_j
  bitrates: [10, 15, 20]              # d^j
  max_flows_per_server: [[5, 4, 3], [6, 5, 4], [5, 5, 5]]  # K^i_j

admission_policy:
  type: "simple_heuristic"
  utility_threshold: 0.1
```

## Key Parameters (Paper Notation)

Following Fox et al.:

- **M**: Number of geographic areas
- **N**: Number of edge servers
- **J**: Set of flow classes {1, ..., M}
- **Q_j**: Arrival rate (Poisson intensity) for class j
- **1/μ_j**: Mean flow duration for class j
- **d^j**: Bitrate requirement for class j flows
- **θ^i**: Access bandwidth capacity of server i
- **K^i_j**: Maximum concurrent flows of class j on server i
- **S(t)**: System state at time t
- **I(t)**: Destination server for incoming flow
- **A(S(t), I(t))**: Admission decision (0=reject, 1=accept)
- **r_j(s,a)**: Reward/utility function

## Metrics Tracked

- Total flows arrived (per class, per area)
- Flows admitted/rejected (per class, per server)
- Server utilization (computing and bandwidth)
- Average active flows per server
- System-wide utility/revenue
- Admission and rejection rates

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_simulator.py -v

# Run with coverage
pytest --cov=src tests/
```

## Examples

See `examples/` directory for:
- `basic_simulation.py`: Simple 3-server, 4-area example
- `multi_class_simulation.py`: Multiple flow classes
- `custom_policy.py`: Implementing custom admission policies

## Documentation

- **[DESIGN.md](docs/DESIGN.md)**: Detailed architecture and design decisions
- **[USAGE.md](docs/USAGE.md)**: Comprehensive usage guide and examples

## Research Reference

This implementation is based on:

**A. Fox, F. De Pellegrini, F. Faticanti, E. Altman, and F. Bronzino**  
*"Optimal Flow Admission Control in Edge Computing via Safe Reinforcement Learning"*  
IEEE WiOPT 2024, Seoul, South Korea

The simulator provides the environment framework described in Section II (System Model) of the paper.

## License

MIT License - see LICENSE file for details

## Authors

- Azeddine Belilita (@Azeddinebelilita)

## Course Information

**Applications of Research and Innovation 2025/2026**  
Instructors: Cleque-Marlain Mboulou-Moutoubi and Francesco De Pellegrini

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## Acknowledgments

Based on research in edge computing admission control and reinforcement learning for network optimization.
