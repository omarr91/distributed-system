import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor


class Scheduler:
    def __init__(self, load_balancer):
        self.lb = load_balancer
        self.queue = Queue()

        # limit parallel tasks
        self.executor = ThreadPoolExecutor(max_workers=20)

        # listener thread
        t = threading.Thread(target=self.process_queue, daemon=True)
        t.start()

    def handle_request(self, request):
        response_queue = Queue()
        self.queue.put((request, response_queue))
        return response_queue.get()

    def process_queue(self):
        while True:
            request, response_queue = self.queue.get()

            # submit task to pool
            self.executor.submit(self.handle_task, request, response_queue)

            self.queue.task_done()

    def handle_task(self, request, response_queue):
        try:
            response = self.lb.dispatch(request)
        except Exception as e:
            print(f"[Scheduler] Error: {e}")
            response = {"id": request.id, "result": "FAILED", "latency": 0}

        response_queue.put(response)