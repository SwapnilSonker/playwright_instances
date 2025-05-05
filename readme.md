# command to run different servers

uvicorn backend:app --host 0.0.0.0 --port 5001
uvicorn backend:app --host 0.0.0.0 --port 5002
uvicorn backend:app --host 0.0.0.0 --port 5003

# command to run main load balancer
uvicorn load2:app --host 0.0.0.0 --port 5000

# api to hit for testing
curl http://localhost:5000/test