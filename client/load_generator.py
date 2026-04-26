import threading
from common.models import Request
from monitoring.metrics import Metrics

def simulate_user(scheduler, user_id, metrics):
    request = Request(id=user_id, query=f"Query {user_id}")
    response = scheduler.handle_request(request)

    metrics.record(response["latency"])

    print(f"[Client] Response {response['id']} | Latency: {response['latency']:.3f}s")


def run_load_test(scheduler, num_users=1000):
    threads = []
    metrics = Metrics()

    metrics.start()

    for i in range(num_users):
        t = threading.Thread(target=simulate_user, args=(scheduler, i, metrics))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    metrics.end()
    metrics.report()