# client/load_generator.py

import threading
from common.models import Request

def simulate_user(scheduler, user_id, result_list=None):
    request = Request(id=user_id, query=f"Query {user_id}")
    response = scheduler.handle_request(request)
    if(result_list != None):
        result_list.put(response)
        return
    return response
