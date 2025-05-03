from fastapi import FastAPI , Request
import httpx
import random
import time

BACKEND_SERVERS = [
    "http://localhost:5001",  # Backend 1
    "http://localhost:5002",  # Backend 2
    "http://localhost:5003",  # Backend 3
]

server_connections = [4,6,2]
server_health = [True , True  , True]

app = FastAPI()

async def health_backend(server_url:str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{server_url}/health")
            return response.status_code == 200
        except:
            return False


def update_server_connections(backend: str , increase : bool = True):
    index = BACKEND_SERVERS.index(backend)

    if increase:
        server_connections[index] += 1
    else:
        server_connections[index] -= 1    


def least_connection_backend() -> str:

    min_connection = min(server_connections)
    print(f"min_connection : {min_connection}")
    server_index = server_connections.index(min_connection)
    print(f"server index : {server_index}")
    backend = BACKEND_SERVERS[server_index]
    print(f"backend : {backend}")
    return backend


@app.api_route("/{path_name:path}" , methods = ["GET" , "POST" , "PUT" , "DELETE"])
async def load_balancer(request: Request , path_name: str):
    healthy_backend = [server for server in BACKEND_SERVERS if await health_backend(server)]
    print(f"Healthy backend : {healthy_backend}")

    if not healthy_backend:
        return {"detail" : "All backend servers are down"}, 503

    backend = least_connection_backend()

    print(f"Forwarding request to backend server : {backend}") 

    update_server_connections(backend , True)

    print(f"server_connections : {server_connections}")

    url = f"{backend}/{path_name}"

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            response = await client.get(url , params = request.query_params)
        elif request.method == "POST":
            response = await client.get(url, json = await request.json())
        elif request.method == "PUT":
            response = await client.get(url, json = await request.json())           
        elif request.method == "DELETE":
            response = await client.delete(url)   

    # update_server_connections(backend, False)  
    # print(f"server connection after : {server_connections}")       

    return response.content , response.status_code        