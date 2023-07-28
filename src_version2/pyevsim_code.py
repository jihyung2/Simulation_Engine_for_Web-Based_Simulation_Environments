from tkinter.tix import Form
from urllib.request import Request

from pyevsim import BehaviorModelExecutor, Infinite, SystemSimulator
from fastapi.responses import JSONResponse
import asyncio
from fastapi import FastAPI, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
import requests

class SimulationModel(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        super().__init__(instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Simulate", 1)
        self.routes = {}
        self.app = FastAPI()  # FastAPI 애플리케이션 객체 생성
        self.router = APIRouter
    def route_show(self):
        return self.app.routes

    def POST_add_route_and_update_app(self, app: FastAPI, route_path: str, response_data: dict):
        @app.post(route_path)
        async def dynamic_route():
            return {"status": "Real POST success","method": "POST","route_path" : route_path, "data": response_data}

        return app.routes[-1]

    def GET_add_route_and_update_app(self, app: FastAPI, route_path: str, response_data: dict):
        @app.get(route_path)
        async def dynamic_route():
            return {"status": "Real GET success", "method": "GET","route_path" : route_path, "data": response_data}

        return app.routes[-1]

    async def register_dynamic_routers(self, route_path, response_data, method):
        router = APIRouter()
        upload = "OK"
        for route_obj in self.app.routes:
            # 각 Route 객체로부터 속성들을 추출합니다.
            path = route_obj.path
            if path == route_path:
                user_route_path = path
                upload = None

        if upload == None:
            print("이미 등록된 경로입니다. 입력된 경로로 데이터를 보내 결과값을 반송합니다.")

            return user_route_path, response_data, method

        else:
            if method == "GET":
                print("GET 라우터로 등록되었습니다.")

                @router.get(route_path)
                async def dynamic_get_route_handler(route_path, response_data):
                    return {"route_path": route_path, "method": "GET", "data": response_data, "test": "GET success"}

                response_data = await dynamic_get_route_handler(route_path, response_data)
                print(response_data)


            elif method == "POST":
                print("POST 라우터로 등록되었습니다.")

                @router.post(route_path)
                async def dynamic_post_route_handler(route_path, response_data):
                    return {"route_path": route_path, "method": "POST", "data": response_data, "test": "POST success"}
                response_data = await dynamic_post_route_handler(route_path, response_data)
                print(response_data)

            self.app.include_router(router)
            print("종료시 등록된 라우터:", self.app.routes)
            print("정상적으로 route가 등록 및 실행되었습니다!")

            return response_data

    async def add_route(self, route_path, response_data):

        parsed_data = self.parse_data(route_path, response_data)
        self.routes = parsed_data
        response = await self.register_dynamic_routers(self.routes["route_path"], self.routes["data"], self.routes["method"])

        return response

    def parse_data(self, route_path, response_data):
        parsed_data = {"route_path": "", "data": {}, "method": ""}

        if "?" in route_path:
            parsed_data["method"] = "GET"
            user_route_path, raw_data = route_path.split("?")
            parsed_data["route_path"] = user_route_path

            data_pairs = raw_data.split("&")
            for data_pair in data_pairs:
                name, value = data_pair.split("=")
                parsed_data["data"][name] = value
        else:
            parsed_data["method"] = "POST"
            parsed_data["route_path"] = route_path
            parsed_data["data"] = {"data": response_data}

        return parsed_data

    async def simulate(self, route_path, response_data):
        simulation_ss = SystemSimulator()
        simulation_ss.register_engine("simulation", "REAL_TIME", 1)
        simulation_ss.get_engine("simulation").insert_input_port("start_simulation")
        simulation_model = SimulationModel(0, Infinite, "SimulationModel", "simulation")
        simulation_ss.get_engine("simulation").register_entity(simulation_model)
        simulation_ss.get_engine("simulation").coupling_relation(None, "start_simulation", simulation_model, "start_simulation")
        print("시작시 등록된 라우터:", self.app.routes)
        async def run_simulation():
            simulation_ss.get_engine("simulation").simulate(5)
            return await self.add_route(route_path, response_data)

        result = await run_simulation()
        return result


