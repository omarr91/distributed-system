from queue import Queue
import threading

class Scheduler:
    def __init__(self, load_balancer):
        self.lb = load_balancer
        self.queue = Queue()

        # background thread
        self.worker_thread = threading.Thread(target=self.process_queue)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def handle_request(self, request):
        print(f"[Scheduler] Dispatching request {request.id}")
        response_queue = Queue()

        self.queue.put((request,response_queue))

        return response_queue.get()
    
    def process_queue(self):
        while 1:
            request,response_queue = self.queue.get()
            response = self.lb.dispatch(request)
            response_queue.put(response)