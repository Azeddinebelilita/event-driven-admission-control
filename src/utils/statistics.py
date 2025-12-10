import pandas as pd
from collections import defaultdict
from typing import Dict, Any

class Statistics:
    """Collects and reports simulation metrics."""
    def __init__(self):
        self.total_arrivals = 0
        self.total_accepted = 0
        self.total_rejected = 0
        
        # Per class metrics
        self.arrivals_by_class = defaultdict(int)
        self.accepted_by_class = defaultdict(int)
        self.rejected_by_class = defaultdict(int)
        
        # Per server metrics
        self.server_load_history = []  # Time-series data
        
        # System utility
        self.total_utility = 0.0

    def record_arrival(self, flow_class: int):
        self.total_arrivals += 1
        self.arrivals_by_class[flow_class] += 1

    def record_admission(self, flow_class: int, server_id: int):
        self.total_accepted += 1
        self.accepted_by_class[flow_class] += 1

    def record_rejection(self, flow_class: int):
        self.total_rejected += 1
        self.rejected_by_class[flow_class] += 1

    def record_server_state(self, time: float, server_id: int, active_flows: int, bandwidth_usage: float):
        self.server_load_history.append({
            'time': time,
            'server_id': server_id,
            'active_flows': active_flows,
            'bandwidth_usage': bandwidth_usage
        })

    def print_summary(self):
        print("\n=== Simulation Results ===")
        print(f"Total Arrivals: {self.total_arrivals}")
        print(f"Total Accepted: {self.total_accepted}")
        print(f"Total Rejected: {self.total_rejected}")
        if self.total_arrivals > 0:
            rate = (self.total_accepted / self.total_arrivals) * 100
            print(f"Global Acceptance Rate: {rate:.2f}%")
        
        print("\nBy Class:")
        for cls in sorted(self.arrivals_by_class.keys()):
            arr = self.arrivals_by_class[cls]
            acc = self.accepted_by_class[cls]
            if arr > 0:
                print(f"  Class {cls}: {acc}/{arr} ({acc/arr*100:.1f}%)")

    def export_to_csv(self, filepath: str):
        if not self.server_load_history:
            return
        df = pd.DataFrame(self.server_load_history)
        df.to_csv(filepath, index=False)
        print(f"Detailed statistics exported to {filepath}")
