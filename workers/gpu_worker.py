import time
import random
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from llm.inference import run_llm
from rag.retriever import retrieve_context

class GPUWorker:
    def __init__(self, id, failure_rate=0.1, max_parallel=4):
        self.id = id
        self.active_requests = 0
        self.total_latency = 0
        self.completed_requests = 0
        self.is_alive = True
        self.failure_rate = failure_rate

        # Queue and parallel processing
        self.request_queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_parallel)
        self.lock = threading.Lock()

        # Start the queue listener
        self._start_queue_listener()

    def avg_latency(self):
        if self.completed_requests == 0:
            return 0
        return self.total_latency / self.completed_requests

    def simulate_failure(self):
        if random.random() < self.failure_rate:
            self.is_alive = False
            raise Exception(f"[Worker {self.id}] ❌ Simulated failure!")

    def _process_internal(self, request, result_container):
        """Actually processes the request and stores result."""
        with self.lock:
            self.active_requests += 1

        start = time.time()
        print(f"[Worker {self.id}] Processing request {request.id}")

        self.simulate_failure()

        context = retrieve_context(request.query)
        result = run_llm(request.query, context)

        latency = time.time() - start

        with self.lock:
            self.total_latency += latency
            self.completed_requests += 1
            self.active_requests -= 1

        result_container["result"] = {
            "id": request.id,
            "result": result,
            "latency": latency
        }

    def _start_queue_listener(self):
        """Background thread that continuously pulls from the queue."""
        def listener():
            while self.is_alive:
                request, result_container, done_event = self.request_queue.get()
                self.executor.submit(self._process_internal, request, result_container)
                self.request_queue.task_done()
                done_event.set()

        t = threading.Thread(target=listener, daemon=True)
        t.start()

    def process(self, request):
        if not self.is_alive:
            raise Exception(f"[Worker {self.id}] is dead. Cannot process request.")

        result_container = {}
        done_event = threading.Event()

        # Push to queue instead of processing directly
        self.request_queue.put((request, result_container, done_event))

        # Wait for the result
        done_event.wait()

        if not result_container.get("result"):
            raise Exception(f"[Worker {self.id}] failed to produce a result.")

        return result_container["result"]