from fastapi import FastAPI
import random
import time

app = FastAPI()

@app.get("/")
async def read_root():
    time.sleep(random.uniform(0.1 , 0.5))

    return {"message" : "Hello from Backend Server"}

# /test route
@app.get("/test")
async def test():
    return {"message": "Test endpoint hit successfully"}

# Example of another endpoint
@app.get("/anotherpath")
async def anotherpath():
    return {"message": "Another path response from the backend"}    

@app.get("/health")
async def health_check():
    return {"status" : "OK"}    