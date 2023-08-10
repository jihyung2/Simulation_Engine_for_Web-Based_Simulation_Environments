import asyncio
import importlib
import asyncio
from multiprocessing import Process, Queue

from fastapi import BackgroundTasks, File
from fastapi import FastAPI, Body, WebSocket, WebSocketDisconnect, websockets
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.staticfiles import StaticFiles

pyevsim_code = importlib.import_module("pyevsim_code")
MyRouter = pyevsim_code.MyRouter
BehaviorModelExecutor = pyevsim_code.BehaviorModelExecutor
Infinite = pyevsim_code.Infinite
my_router = MyRouter(0, Infinite, "MyRouter", "Engine1")

app = FastAPI()


class WebhookData(BaseModel):
    checkboxes: List[str]
    port: int
    username: str
    time: str


webhook_result = []

def simulate_process(request_data, result_queue):
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

    # 시뮬레이션 결과를 가져옴
    simulation_results = []

    while not result_queue.empty():
        simulation_result = result_queue.get()
        simulation_results.append(simulation_result)

    print("All Simulations Complete!")
    print("Simulation Results:", simulation_results)
    return {"message": "All Simulations run!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8900)