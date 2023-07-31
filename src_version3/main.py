import asyncio
import importlib
import asyncio
from multiprocessing import Process, Queue

from fastapi import BackgroundTasks
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

def simulate_process(request_data, result_queue):
    # 이곳에 시뮬레이션 로직을 구현
    # 시뮬레이션 결과를 result_queue에 넣음
    # 예시로 단순히 request_data를 그대로 전달하는 예시
    abc = my_router.simulate(request_data)
    result_queue.put(abc)

@app.post("/start_simulation")
async def start_simulation(request: Request):
    request_data = await request.json()
    print(request_data)

    # 결과를 저장할 큐 생성
    result_queue = Queue()
    # 멀티 프로세스로 시뮬레이션 실행
    processes = []

    for data in request_data:
        process = Process(target=simulate_process, args=(data, result_queue))
        process.start()
        processes.append(process)

    # 모든 프로세스가 종료될 때까지 대기
    for process in processes:
        process.join()

    # 시뮬레이션 결과를 가져옴
    simulation_results = []
    while not result_queue.empty():
        simulation_result = result_queue.get()
        simulation_results.append(simulation_result)

    print("All Simulations Complete!")
    print("Simulation Results:", simulation_results)
    return {"message": "All Simulations Complete!"}


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