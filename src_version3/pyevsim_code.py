import asyncio
from multiprocessing import Process

from anyio import run
import http
import json
import time
import datetime
from asyncio import ensure_future, get_event_loop
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from urllib.parse import urlparse

import aiohttp
import httpx
import requests
from fastapi import FastAPI, Request, Form, APIRouter
from pyevsim import BehaviorModelExecutor, Infinite, SystemSimulator
import pyevsim

app = FastAPI()
global a
global realdata
a = "dummy"
class MyRouter(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        super().__init__(instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state(a, 1)
        self.insert_state("simulation Start", 1)

    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "simulation Start"

    def output(self):
        now = datetime.datetime.now()
        self.index = 0
        self.item_list = []

        if hasattr(self, "menu"):
            for i in range(len(self.menu)):
                self._cur_state, self.temp = self.int_trans()
                self.item_list.append(int(self.temp))
                self.index += 1
            print("==========================\n"
                  f"{self.menu}\n"
                  f"{self.item_list}\n"
                  f"{now}")
            self.put_db(self.item_list)


        else:
            print("메뉴가 아직 생성되지 않았습니다.")

        self.item_list = []
        self.index = 0
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
                # 이벤트 발생시 여기 출력
                def sync_webhook_send(request_data):
                    now = datetime.datetime.now()
                    webhook_url = f"http://127.0.0.1:{request_data['port']}/{request_data['username']}"
                    webhook_data = request_data
                    webhook_data["time"] = str(now)
                    try:
                        response = requests.post(webhook_url, json=webhook_data)
                        if response.status_code == 200:
                            print("성공")
                        else:
                            print("실패")
                    except Exception as e:
                        print(f"웹훅 요청 중 오류 발생: {e}")

                sync_webhook_send(realdata)
                return self.menu[self.index], 100
            else:
                #이벤트 없을때도 출력( 실험용 )
                def sync_webhook_send(request_data):
                    now = datetime.datetime.now()
                    webhook_url = f"http://127.0.0.1:{request_data['port']}/{request_data['username']}"
                    webhook_data = request_data
                    webhook_data["time"] = str(now)
                    try:
                        response = requests.post(webhook_url, json=webhook_data)
                        if response.status_code == 200:
                            print("성공")
                        else:
                            print("실패")
                    except Exception as e:
                        print(f"웹훅 요청 중 오류 발생: {e}")
                #쓰레드 형식으로 하지 않아도 동기식으로 작동되지 않아 블로킹되지 않기 때문에 그냥 사용해도 가능하다.
                #괜히 쓰레드 사용해서 더 낭비만 하지말고 정석으로 이벤트 발생 -> 웹훅 방식 사용
                #thread = Thread(target=sync_webhook_send, args=(realdata,))
                #thread.start()
                sync_webhook_send(realdata)
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


    async def clear_data(self):
        ss = SystemSimulator()
        ss.register_engine("api", "DISCRETE_EVENT", 1)

    async def destruct(self):
        await self.clear_data()
