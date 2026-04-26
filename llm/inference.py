import time
import random

def run_llm(query, context):
    # Simulate GPU inference delay
    time.sleep(random.uniform(0.2,5.0))
    return f"LLM Answer to '{query}' using [{context}]"