import importlib
import time
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from pyevsim import BehaviorModelExecutor, Infinite, SystemSimulator
import asyncio
import requests
import uvicorn
import aiohttp

# FastAPI와 Pyevsim 모두 정상적으로 불러오는지 확인
try:
    print("fastapi 생성 완료")
    app = FastAPI()
    router = APIRouter()
    templates = Jinja2Templates(directory="templates")

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
except Exception as e:
    app = None
    print("FastAPI 에러 발생", str(e))


try:
    pyevsim_code = importlib.import_module("pyevsim_code")
    SimulationModel = pyevsim_code.SimulationModel
    BehaviorModelExecutor = pyevsim_code.BehaviorModelExecutor
    Infinite = pyevsim_code.Infinite

    simulation_model = SimulationModel(0, Infinite, "SimulationModel", "simulation")
    print("pyevsim 생성 완료")
    pyevsim_error = False

except ImportError:
    simulation_model = None
    pyevsim_error = True
    print("pyevsim 모듈이 존재하지 않습니다.")

except Exception as d:
    simulation_model = None
    pyevsim_error = True
    print("pyevsim 에러 발생", str(d))

# FastAPI와 Pyevsim 모두 정상적으로 불러온 경우
if app and simulation_model:
    @app.post("/start_simulation")
    async def start_simulation(route_path: str = Form(...), data: str = Form(...)):
        response = await simulation_model.simulate(route_path, data) # 동적 라우터 등록
        print(response)
        if isinstance(response, dict):
            if response.get("method") == "POST":  # 동적 라우터 실행
                new_route = simulation_model.POST_add_route_and_update_app(app, response["route_path"], response["data"])
                print(new_route)


            elif response.get("method") == "GET":
                new_route = simulation_model.GET_add_route_and_update_app(app, response["route_path"], response["data"])
                print(new_route)


        elif isinstance(response, tuple):
            url = str("http://localhost:8700"+response[0])
            response = await fastapi_send(url, response[1], response[2])

        return response


    async def fastapi_send(url: str, data: dict, method: str):
        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(url) as response:
                    response_data = await response.json()
            elif method == "POST":
                async with session.post(url, json=data) as response:
                    response_data = await response.json()

        print(response_data)
        return response_data


    if __name__ == "__main__":
        uvicorn.run(app, host="127.0.0.1", port=8700)

# Pyevsim만 정상적으로 불러온 경우
elif simulation_model:
    route_path = input("경로")
    route_path = input("데이터")
    async def start_simulation(route_path: str = Form(...), data: str = Form(...)):
        response = await simulation_model.simulate(route_path, data)

        if response["method"] == "POST":  # 동적 라우터 실행
            new_route = simulation_model.POST_add_route_and_update_app(app, response["route_path"], response["data"])
            print(new_route)

        elif response["method"] == "GET":
            new_route = simulation_model.GET_add_route_and_update_app(app, response["route_path"], response["data"])
            print(new_route)

        return response

# FastAPI만 정상적으로 불러온 경우
elif app:
    @app.post("/start_simulation")
    async def handle_web_hook(route_path: str = Form(...), data: str = Form(...)):
        response = {"message": "pyevsim이 죽어서 fast api로만 보냅니다.", "data": data}
        return response

    print("Fast API만 실행됩니다.")
    uvicorn.run(app, host="127.0.0.1", port=8700)

# Pyevsim과 FastAPI 모두 에러가 발생한 경우
else:
    print("Pyevsim과 Fast API가 모두 에러가 발생했습니다.")
