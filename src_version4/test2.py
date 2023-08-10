from pyevsim import BehaviorModelExecutor, Infinite, SystemSimulator
from fastapi.responses import JSONResponse
import asyncio
from fastapi import FastAPI, Request, Form, APIRouter
import fastapi_code

class SimulationModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Simulate", 1)
        self.routes = {}  # 동적으로 추가되는 라우터를 저장하는 딕셔너리

    def add_route(self, route_path, response_data):

        # 라우터를 추가하는 메서드
        parsed_data = self.parse_data(route_path, response_data)
        if parsed_data["method"] == "GET":
            # GET 방식의 경우 handle_get_response 호출
            print("GET 라우터로 등록되었습니다.")
            self.routes = parsed_data

            print(self.routes)

            return self.routes

        elif parsed_data["method"] == "POST":
            print("POST 라우터로 등록되었습니다.")
            # POST 방식의 경우 handle_post_response 호출
            self.routes = parsed_data
            print(self.routes)

            return self.routes


    def parse_data(self, route_path, response_data):
        # 웹에서 받은 데이터를 분석하여 필요한 정보를 추출하는 메서드

        parsed_data = {"route_path": "", "data": {}, "method": ""}

        if "?" in route_path:
            # GET 방식
            parsed_data["method"] = "GET"
            user_route_path, raw_data = route_path.split("?")
            parsed_data["route_path"] = user_route_path

            # '&'로 데이터 분리
            data_pairs = raw_data.split("&")
            for data_pair in data_pairs:
                # '='로 이름과 값 분리
                name, value = data_pair.split("=")
                parsed_data["data"][name] = value
        else:
            # POST 방식
            parsed_data["method"] = "POST"
            parsed_data["route_path"] = route_path
            parsed_data["data"] = {"data": response_data}

        return parsed_data

    async def simulate(self, route_path, response_data):
        try:
            simulation_ss = SystemSimulator()
            simulation_ss.register_engine("simulation", "REAL_TIME", 1)
            simulation_ss.get_engine("simulation").insert_input_port("start_simulation")
            simulation_model = SimulationModel(0, Infinite, "SimulationModel", "simulation")
            simulation_ss.get_engine("simulation").register_entity(simulation_model)
            simulation_ss.get_engine("simulation").coupling_relation(None, "start_simulation", simulation_model,
                                                                     "start_simulation")

            async def run_simulation():
                simulation_ss.get_engine("simulation").simulate(5)
                simulation_model.add_route(route_path, response_data)
                return self.routes

            print("return await run_simulation(): " + str(run_simulation))
            return await run_simulation()

        except Exception as e:
            print("pyevsim에서 에러 발생:", str(e))
            return None


async def simulation_model():
    try:
        app = FastAPI()
        router = APIRouter()

        simulation_model = SimulationModel(0, Infinite, "SimulationModel", "simulation")

        # 시뮬레이션 모델에 라우터 추가
        await simulation_model.simulate("/test","Test response") #POST방식
        await simulation_model.simulate("/api?data1=value1&data2=value2", "") #GET방식


    except Exception as e:
        print("테스트 도중 오류 발생:", str(e))

# 테스트 수행
asyncio.run(simulation_model())