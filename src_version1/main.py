import asyncio
import importlib

from fastapi import FastAPI, Body, WebSocket, WebSocketDisconnect, websockets
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi import FastAPI, Request, Form, APIRouter

pyevsim_code = importlib.import_module("pyevsim_code")
MyRouter = pyevsim_code.MyRouter
BehaviorModelExecutor = pyevsim_code.BehaviorModelExecutor
Infinite = pyevsim_code.Infinite
my_router = MyRouter(0, Infinite, "MyRouter", "Engine1")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class WebData(BaseModel):
    checkboxes: List[str]
    port: int
    username: str


class WebhookData(BaseModel):
    checkboxes: List[str]
    port: int
    username: str
    time: str


webhook_result = []


@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/start_simulation")
async def start_simulation(data: WebData):
    print(data)
    await my_router.simulate(data)


@app.post("/{username}")
async def receive_webhook(username: str, webhook_data: WebhookData):
    global webhook_result
    print("웹훅 데이터 수신:")
    print(f"체크박스: {webhook_data.checkboxes}")
    print(f"포트: {webhook_data.port}")
    print(f"사용자 이름: {webhook_data.username}")
    print(webhook_data.time)
    webhook_result.append(webhook_data.dict())


@app.get("/get_result")
async def get_result():
    global webhook_result
    if webhook_result:
        data = webhook_result[-1]
    else:
        data = None
    return JSONResponse(content={"result": data})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8900)