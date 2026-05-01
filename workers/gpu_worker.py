import time
from llm.inference import run_llm
from rag.retriever import retrieve_context


class GPUWorker:
    def __init__(self, id):
        self.id = id
        self.active_requests = 0
        self.total_latency = 0
        self.completed_requests = 0

    def avg_latency(self):
        if self.completed_requests == 0:
            return 0
        return self.total_latency / self.completed_requests

    def process(self, request):
        self.active_requests += 1
        start = time.time()

        print(f"[Worker {self.id}] Processing request {request.id}")

        context = retrieve_context(request.query)
        result = run_llm(request.query, context)

        latency = time.time() - start

        self.total_latency += latency
        self.completed_requests += 1
        self.active_requests -= 1

        return {
            "id": request.id,
            "worker_id": self.id,
            "result": result,
            "latency": latency
        }