class LoadAwareLB:
    def __init__(self, workers):
        self.workers = workers

    def get_score(self, worker):
        # lower score = better worker
        return (worker.active_requests * 0.7) + (worker.avg_latency() * 0.3)

    def get_next_worker(self):
        worker = min(self.workers, key=lambda w: self.get_score(w))
        print(f"[LB] LoadAware → Worker {worker.id} | Score: {self.get_score(worker):.3f}")
        return worker

    def dispatch(self, request):
        worker = self.get_next_worker()
        return worker.process(request)