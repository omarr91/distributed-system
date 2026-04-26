class LeastConnectionsLB:
    def __init__(self, workers):
        self.workers = workers

    def get_next_worker(self):
        worker = min(self.workers, key=lambda w: w.active_requests)
        print(f"[LB] LeastConnections → Worker {worker.id}")
        return worker

    def dispatch(self, request):
        worker = self.get_next_worker()
        return worker.process(request)