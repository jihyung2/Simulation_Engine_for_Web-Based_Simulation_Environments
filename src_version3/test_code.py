from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from pyevsim import BehaviorModelExecutor, Infinite, SystemSimulator
import asyncio
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 웹 페이지(프론트엔드) 렌더링
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 시뮬레이션 수행을 위한 Pyevsim 모델링
class SimulationModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Simulate", 1)
        self.is_post = False
        self.msg = None

    def ext_trans(self, port, msg):
        if port == "start_simulation":
            self._cur_state = "Simulate"
            if msg.get("data"):
                self.msg = msg.get("data")
                self.is_post = True
            else:
                self.is_post = False

    def output(self):
        print(self.is_post)
        if self.is_post:
            simulation_result = {"message": "Simulation result", "data": self.msg}
            print("json 있음 -> post 전송")
            backend_url = "http://backend_server_url"  # 백엔드 서버의 URL을 넣으세요
            response_backend = requests.post(backend_url, json=simulation_result)
        else:
            simulation_result = {"message": "Simulation result (GET)", "data": self.msg}
            print("json 없음 -> get 전송")
            print(simulation_result)
            response = JSONResponse(content=simulation_result)
            print(response)
            backend_url = "http://backend_server_url"  # 백엔드 서버의 URL을 넣으세요
            response_backend = requests.get(backend_url, params=simulation_result)

        if response_backend.status_code == 200:
            print("백엔드 서버 응답:", response_backend.json())

        return simulation_result

# 웹 페이지에서 POST 요청을 받는 라우터
@app.post("/start_simulation")
async def start_simulation(data: str = Form(...)):
    simulation_ss = SystemSimulator()
    simulation_ss.register_engine("simulation", "REAL_TIME", 1)
    simulation_ss.get_engine("simulation").insert_input_port("start_simulation")
    simulation_model = SimulationModel(0, Infinite, "SimulationModel", "simulation")
    simulation_ss.get_engine("simulation").register_entity(simulation_model)
    simulation_ss.get_engine("simulation").coupling_relation(None, "start_simulation", simulation_model, "start_simulation")
    print("시뮬레이션에 들어가는 데이터:", data)

    # 비동기적으로 시뮬레이션 실행
    async def run_simulation():
        simulation_ss.get_engine("simulation").simulate(5)
        simulation_model.ext_trans("start_simulation", {"data": data})
        result = simulation_model.output()
        response = JSONResponse(content=result)
        print(response)
        return response

    return await run_simulation()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)