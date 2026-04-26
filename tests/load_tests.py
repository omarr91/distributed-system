from monitoring.metrics import Metrics
from client.load_generator import simulate_user
import threading

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