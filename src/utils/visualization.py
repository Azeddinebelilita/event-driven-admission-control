import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for file saving
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict

class Visualizer:
    @staticmethod
    def plot_server_utilization(server_load_history: List[Dict], output_file: str = 'results_utilization.png'):
        """Plots bandwidth usage over time for each server."""
        if not server_load_history:
            print("No server history to plot.")
            return

        df = pd.DataFrame(server_load_history)
        
        plt.figure(figsize=(10, 6))
        
        # Get unique servers
        servers = df['server_id'].unique()
        
        for server_id in servers:
            server_data = df[df['server_id'] == server_id]
            # Sort by time just in case
            server_data = server_data.sort_values('time')
            plt.plot(server_data['time'], server_data['bandwidth_usage'], label=f'Server {server_id}')
            
        plt.xlabel('Time (s)')
        plt.ylabel('Bandwidth Usage')
        plt.title('Server Bandwidth Utilization Over Time')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_file)
        print(f"Saved utilization plot to {output_file}")
        plt.close()

    @staticmethod
    def plot_acceptance_rates(stats_obj, output_file: str = 'results_metrics.png'):
        """Plots acceptance vs rejection counts per class."""
        classes = sorted(stats_obj.arrivals_by_class.keys())
        accepted = [stats_obj.accepted_by_class[c] for c in classes]
        rejected = [stats_obj.rejected_by_class[c] for c in classes]
        
        x = range(len(classes))
        width = 0.35
        
        plt.figure(figsize=(10, 6))
        plt.bar([i - width/2 for i in x], accepted, width, label='Accepted', color='green')
        plt.bar([i + width/2 for i in x], rejected, width, label='Rejected', color='red')
        
        plt.xlabel('Flow Class')
        plt.ylabel('Number of Flows')
        plt.title('Admission Control Results by Class')
        plt.xticks(x, [f'Class {c}' for c in classes])
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(output_file)
        print(f"Saved metrics plot to {output_file}")
        plt.close()
