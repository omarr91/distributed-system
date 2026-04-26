import random

# Simulated knowledge base
KNOWLEDGE_BASE = [
    "Distributed systems use multiple nodes to solve problems together.",
    "Load balancing distributes requests across servers to avoid overload.",
    "GPU clusters accelerate deep learning and LLM inference tasks.",
    "RAG retrieves relevant documents to improve LLM response quality.",
    "Fault tolerance ensures a system keeps running despite node failures.",
    "Round Robin assigns requests to workers in a fixed rotating order.",
    "Least Connections routes to the worker with fewest active requests.",
    "Vector databases store embeddings for fast similarity search.",
    "LLM inference involves running a trained model to generate text.",
    "Scalability means a system handles more load by adding resources.",
]

def retrieve_context(query, top_k=3):
    # Simulate relevance scoring (random score per document)
    scored = [(doc, random.uniform(0.5, 1.0)) for doc in KNOWLEDGE_BASE]
    
    # Sort by score descending (best match first)
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    
    # Return top_k results
    top_results = [doc for doc, score in ranked[:top_k]]
    
    print(f"[RAG] Retrieved {top_k} context chunks for query: '{query}'")
    
    return " | ".join(top_results)