import time
import datetime

import requests
from fastapi import FastAPI, Request, Form, APIRouter
from pyevsim import BehaviorModelExecutor, Infinite, SystemSimulator
import pyevsim

app = FastAPI()
global a
global realdata
a = "dummy data"

#이벤트 기반 시뮬레이션
class MyRouter(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state(a,1)
        self.insert_state("simulation Start", 1)


    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "simulation Start"
            # API 요청 처리 및 상태 변경



    def output(self):
        now = datetime.datetime.now()
        self.index = 0
        self.item_list = []
        print("==========================")
        for i in range(len(self.menu)):
            self._cur_state, self.temp = self.int_trans()
            self.item_list.append(int(self.temp))
            self.index += 1

        print(self.menu)
        print(self.item_list)
        print(now)
        self.web_hook_send(realdata)
        self.put_db(self.item_list)
        self.item_list = []
        self.index = 0


        #if self._cur_state == "API":
            # API 요청에 대한 처리 결과 반환
            #return {"message": "This is the response for API request"}

        #else:
            # 잘못된 API 요청 처리
            #return {"message": "Invalid API request"}
    def web_hook_send(self, request_data):
        webhook_url = f"http://127.0.0.1:{request_data.port}/{request_data.username}"
        webhook_data = request_data.dict()
        print(webhook_url)
        response = requests.post(webhook_url, json = webhook_data)

        if response.status_code == 200:
            print("성공")
        else:
            print("실패")

    def insert_list(self, arr):
        setattr(self, "menu", arr)
        setattr(self, "index", 0)
        setattr(self, "temp", 0)

    def put_db(self, item_list):
        pass

    def int_trans(self):
        now = datetime.datetime.now()
        if self.menu[self.index] == str(a):
            if str(a) == "/api":
                return self.menu[self.index], 100

            else:
                return self.menu[self.index], 0

    def simulate(self, request_data):
        global a
        global realdata
        realdata = request_data
        a = str(request_data)
        print("Simulating...")
        menu = [a]
        ss = SystemSimulator()
        ss.register_engine("first", "REAL_TIME", 1)
        ss.get_engine("first").insert_input_port("start")
        gen = MyRouter(0, Infinite, "Gen", "first")
        gen.insert_list(menu)
        ss.get_engine("first").register_entity(gen)
        ss.get_engine("first").coupling_relation(None, "start", gen, "start")
        ss.get_engine("first").insert_external_event("start", None)
        ss.get_engine("first").simulate()

    def clear_data(self):
        ss = SystemSimulator()
        ss.register_engine("api", "DISCRETE_EVENT", 1)

    def destruct(self):
        #미완성
        self.clear_data()

