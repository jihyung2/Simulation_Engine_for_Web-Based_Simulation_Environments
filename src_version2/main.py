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

@app.post("/start_simulation")
async def start_simulation(data: WebData):
    # 웹훅을 사용하여 시뮬레이션 처리를 시작합니다.
    print(data)
    my_router.simulate(data)
    web_hook_receive(data)
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8700)

@app.post("/{data.username}")
async def web_hook_receive(data):


    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=data.port)