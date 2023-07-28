from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime
import time
import pymysql
import sys
import socket
import json
sys.path.append('C:\\capstone\\')
import requests
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

n=0

class PEx(BehaviorModelExecutor):

    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name,
                                       engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        # self.insert_state("Generate", 1)
        self.insert_state("UpdateServer_Start", 1)
        self.insert_state("Google_Upload", 1)
        self.insert_state("DB_Upload", 1)
        self.insert_state("AIlearning", 1)
        self.insert_state("Chatbot_Update", 1)
        self.insert_input_port("start")

        # self.custom_date = ''

    def ext_trans(self, port, msg):
        if port == "start":
            # print(f"[app started]")
            # print("Date input : ")
            # date_ = input()
            # self.set_date(date_)
            self._cur_state = "UpdateServer_Start"

    def output(self):
        self.index = 0
        self.item_list = []
        print("==========================")
        for i in range(len(self.menu)):
            self._cur_state, self.temp = self.int_trans()
            self.item_list.append(int(self.temp))
            self.index += 1

        print(self.menu)
        print(self.item_list)
        self.put_db(self.item_list)
        self.item_list = []
        self.index = 0
        return None

    def put_db(self, item_list):
        pass

    def int_trans(self):
        now = datetime.datetime.now()
        global n

        if self.menu[self.index] == "GoogleSpreadSheet":
            if now.weekday() == 1 and now.hour == 0 and now.minute == 0:
                db = pymysql.connect(host='127.0.0.1', user='root', password='040416', db='qtdata', charset='utf8',
                                     port=3306)
                cursor = db.cursor(pymysql.cursors.DictCursor)
                n = n + 1
                print(now)
                last_tuesday = now - datetime.timedelta(days=now.weekday(), weeks=1)
                next_monday = last_tuesday + datetime.timedelta(days=6)
                last_tuesday_str = last_tuesday.strftime("%Y-%m-%d 00:00:00")
                next_monday_str = next_monday.strftime("%Y-%m-%d 23:59:59")
                cursor.execute(
                    f"SELECT dataset.*, userinfo.* FROM dataset INNER JOIN userinfo ON dataset.id = userinfo.chatid WHERE dataset.timestamp >= '{last_tuesday_str}' AND dataset.timestamp <= '{next_monday_str}'")
                data = cursor.fetchall()
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive",
                ]
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    'C:/capstone/pythonProject/capdi-378609-2fc18c110369.json',
                    scope)
                client = gspread.authorize(creds)

                week_num = last_tuesday.isocalendar()[1]

                try:
                    worksheet = client.open('capstone_question_data').worksheet(
                        str(n + 12) + "주차")  # 여기 부분에 작성했음 3/21일 기준 +1
                except gspread.exceptions.WorksheetNotFound:
                    worksheet = client.open('capstone_question_data').add_worksheet(title=str(n + 12) + "주차", rows=1,
                                                                                    cols=1)

                keys = ['num', 'name', 'id', 'type', 'question', 'timestamp']

                for row_index, row_data in enumerate(data):
                    row_data_values = [row_data[key] for key in keys]

                    row_data_str = [str(cell) for cell in row_data_values]

                    range_ = f'A{row_index + 2}:{chr(ord("A") + len(row_data_str))}{row_index + 2}'

                    while True:
                        try:
                            worksheet.update(range_, [row_data_str])
                            break
                        except gspread.exceptions.APIError as e:
                            if e.response.status_code == 429:  # rate limit exceeded
                                print("Quota exceeded, waiting...")
                                time.sleep(60)  # wait for 1 minute
                            else:
                                raise e

                print("db --> " + str(n + 12) + "주차 구글 스프레드시트로 성공적으로 입력되었습니다.")
                db.commit()
                db.close()
                time.sleep(60)
                return "Google_Upload", 100

            else:
                return "Google_Upload", 0


        if self.menu[self.index] == "MariaDB":
            if now.weekday() == 2 and now.hour == 0 and now.minute == 0:
                db = pymysql.connect(host='127.0.0.1', user='root', password='040416', db='qtdata', charset='utf8',
                                     port=3306)
                cursor = db.cursor(pymysql.cursors.DictCursor)
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive",
                ]
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    'C:/capstone/pythonProject/capdi-378609-2fc18c110369.json',
                    scope)
                client = gspread.authorize(creds)

                spreadsheet = client.open('capstone_question_data')
                worksheet = spreadsheet.worksheet('학습용질문데이터')
                data = worksheet.get_all_values()

                query = "INSERT INTO testdata (clustering, question, testnum) VALUES (%s, %s, %s)"

                for row in data:
                    cursor.execute(query, (row[0], row[1], row[2]))
                print("구글 스프레드시트 --> db 성공적으로 입력되었습니다.")
                db.commit()
                db.close()
                time.sleep(60)
                return "DB_Upload", 100
            else:
                return "DB_Upload", 0

        if self.menu[self.index] == "AIlearning":
            if now.weekday() == 2 and now.hour == 0 and now.minute == 10:
                print("AI Learning Success!!")
                time.sleep(60)
                return "Chatbot_Update", 100
            else:
                return "Chatbot_Update", 0

        if self.menu[self.index] == "ChatbotUpdate":
            if now.weekday() == 2 and now.hour == 0 and now.minute == 20:
                # 서버 정보
                server_ip = '127.0.0.1'
                server_port = 5050

                # 서버에 연결
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                query = "질문 답변 데이터 업로드"
                # JSON 데이터 생성
                send_json_data = {
                    'Query': query
                }
                message = json.dumps(send_json_data)

                # 데이터 전송
                client_socket.send(message.encode())
                print("Chatbot Update Success!!")
                # 소켓 연결 종료
                client_socket.close()

                server_ip = '127.0.0.1'
                server_port = 5050

                # 서버에 연결
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_ip, server_port))
                query = "ChatBot Auto Update Success!!"
                # JSON 데이터 생성
                send_json_data = {
                    'Query': query
                }
                message = json.dumps(send_json_data)

                # 데이터 전송
                client_socket.send(message.encode())
                print("ChatBot Auto Update Success!!")
                # 소켓 연결 종료
                client_socket.close()



                time.sleep(60)
                return "Chatbot_Update", 100
            else:
                return "Chatbot_Update", 0

    def insert_list(self, arr):
        setattr(self, "menu", arr)
        setattr(self, "index", 0)
        setattr(self, "temp", 0)

def start():
    print("pyevsim_Auto_UpdateServer Start...")
    menu = ['GoogleSpreadSheet', 'MariaDB', 'AIlearning', 'ChatbotUpdate']
    ss = SystemSimulator()
    ss.register_engine("first", "REAL_TIME", 1)
    ss.get_engine("first").insert_input_port("start")
    gen = PEx(0, Infinite, "Gen", "first")
    gen.insert_list(menu)
    ss.get_engine("first").register_entity(gen)
    ss.get_engine("first").coupling_relation(None, "start", gen, "start")
    ss.get_engine("first").insert_external_event("start", None)
    ss.get_engine("first").simulate()



start()