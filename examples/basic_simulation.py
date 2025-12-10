import sys
import os
import yaml

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.simulator.event_simulator import EventDrivenSimulator

def main():
    config_path = os.path.join(os.path.dirname(__file__), '../config/simulation_config.yaml')
    
    print("Loading configuration...")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    print("Initializing simulator...")
    simulator = EventDrivenSimulator(config)
    
    print("Running simulation...")
    stats = simulator.run()
    
    stats.print_summary()
    stats.export_to_csv('simulation_results.csv')

    # Visualization
    from src.utils.visualization import Visualizer
    print("Generating plots...")
    Visualizer.plot_server_utilization(stats.server_load_history, 'results_utilization.png')
    Visualizer.plot_acceptance_rates(stats, 'results_metrics.png')

if __name__ == "__main__":
    main()
