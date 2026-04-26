from lb.round_robin import RoundRobinLB
from lb.least_connections import LeastConnectionsLB
from lb.load_aware import LoadAwareLB

class LoadBalancer:
    def __init__(self, workers, strategy="round_robin"):
        if strategy == "least_connections":
            self.strategy = LeastConnectionsLB(workers)
        elif strategy == "load_aware":
            self.strategy = LoadAwareLB(workers)
        else:
            self.strategy = RoundRobinLB(workers)

        print(f"[LB] Using strategy: {strategy}")

    def dispatch(self, request):
        return self.strategy.dispatch(request)