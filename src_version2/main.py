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
@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start_simulation")
async def start_simulation(data: WebData):
    # 웹훅을 사용하여 시뮬레이션 처리를 시작합니다.
    print(data)
    url = f"http://localhost:{data.port}/{data.username}"
    await my_router.simulate(data)
    print("pass!")
    return {"redirect_url" : url}

@app.post("/{username}")
async def receive_webhook(data):
    print("232323")
    print(data)
    # 필요한 처리를 수행한 후 응답을 반환합니다.
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8700)