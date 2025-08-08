from fastapi import FastAPI
from starlette.responses import StreamingResponse

from fuse import langfuse_handler
from app import orchestrator_worker

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/query/sync/{name}")
async def query_sync(name: str) :
    return orchestrator_worker.stream(name)

@app.get("/query/{name}")
async def query(name: str) :
    return orchestrator_worker.invoke(name, config={"callbacks": [langfuse_handler]})

@app.get("/query/stream/{name}")
async def query_stream(name: str) :
    # 目前不支持
    return StreamingResponse(orchestrator_worker.stream(name))
