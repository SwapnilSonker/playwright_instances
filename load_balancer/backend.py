from fastapi import FastAPI
import random
import time

app = FastAPI()

@app.get("/")
async def read_root():
    time.sleep(random.uniform(0.1 , 0.5))

    return {"message" : "Hello from Backend Server"}

@app.get("/health")
async def health_check():
    return {"status" : "OK"}    