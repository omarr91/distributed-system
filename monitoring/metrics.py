import time

class Metrics:
    def __init__(self):
        self.latencies = []
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def record(self, latency):
        self.latencies.append(latency)

    def report(self):
        total_requests = len(self.latencies)
        avg_latency = sum(self.latencies) / total_requests if total_requests else 0
        max_latency = max(self.latencies) if total_requests else 0
        min_latency = min(self.latencies) if total_requests else 0
        total_time = self.end_time - self.start_time if self.end_time and self.start_time else 1
        throughput = total_requests / total_time

        print("\n=== RESULTS ===")
        print(f"Total Requests: {total_requests}")
        print(f"Average Latency: {avg_latency:.3f}s")
        print(f"Max Latency: {max_latency:.3f}s")
        print(f"Min Latency: {min_latency:.3f}s")
        print(f"Throughput: {throughput:.2f} req/sec")