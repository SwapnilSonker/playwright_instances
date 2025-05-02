from fastapi import FastAPI, Request
import httpx
import random
import time

# List of backend servers (replace these with actual backend IPs or URLs)
BACKEND_SERVERS = [
    "http://localhost:5001",  # Backend 1
    "http://localhost:5002",  # Backend 2
    "http://localhost:5003",  # Backend 3
]

# Simulating server load (number of active connections and response times)
server_connections = [0, 0, 0]
server_response_time = [0, 0, 0]

# Round Robin Index for load balancing
current_backend_index = 0

app = FastAPI()

def simulate_server_load():
    """Simulate server load with random response times."""
    return random.uniform(0.1, 0.5)

def get_next_backend_round_robin() -> str:
    """Round Robin load balancing algorithm."""
    global current_backend_index
    print(f"at start c : {current_backend_index}")
    backend = BACKEND_SERVERS[current_backend_index]
    print(f"at start : {backend}")
    current_backend_index = (current_backend_index + 1) % len(BACKEND_SERVERS)
    print(f"at end : {current_backend_index}")
    return backend

# @app.get("/test")
# async def test_path():
#     return {"message": "This is the test path!"}

@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def load_balancer(request: Request, path_name: str):
    """Load balancer function that forwards requests to backend servers."""
    
    # 1. Round Robin Load Balancing
    backend = get_next_backend_round_robin()
    print(f"Forwarding request to backend: {backend}")

    # Simulate server load (response time)
    server_response_time[BACKEND_SERVERS.index(backend)] = simulate_server_load()
    print(f"server_response_time : {server_response_time}")

    # Construct the URL to forward the request to the selected backend server
    url = f"{backend}/{path_name}"

    # Simulate connection count update for Least Connections (round robin, for now)
    server_connections[BACKEND_SERVERS.index(backend)] += 1
    print(f"server_connections : {server_connections}")

    # Forward the request to the backend server based on the HTTP method
    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            response = await client.get(url, params=request.query_params)
            print(f"GET : {path_name} , {response}")
        elif request.method == "POST":
            response = await client.post(url, json=await request.json())
            print(f"POST : {path_name}")
        elif request.method == "PUT":
            response = await client.put(url, json=await request.json())
            print(f"PUT : {path_name}")
        elif request.method == "DELETE":
            response = await client.delete(url)
            print(f"DELETE : {path_name}")

    # Return the response content from the backend server
    return response.content, response.status_code
