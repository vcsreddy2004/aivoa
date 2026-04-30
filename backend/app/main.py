# app/main.py
from fastapi import FastAPI
from app.schema import HCPInput
from app.agent import app_graph
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate(data: HCPInput):
    result = app_graph.invoke({"text": data.text})
    response = result["data"]

    if "history" in response:
        return {"type": "history", "data": response["history"]}

    if "suggestion" in response:
        return {"type": "followup", "data": response["suggestion"]}

    return {"type": "action", "data": response}