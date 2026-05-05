from transformers import pipeline 

pipe = pipeline("text-generation", model="google/gemma-3-1b-it")
def run_llm(query,context):
    messages = [
    {"role": "user", "content": "Who are you?"},
    ]
    pipe(messages)

run_llm("test","test")