from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse

class MyFastAPI():
    def __init__(self):
        self.app = FastAPI()
    def post(self, path, **kwargs):
        return self.app.post(path, **kwargs)

        #raise Exception("FastAPI 에러 발생")

    def get(self, path, **kwargs):
        return self.app.get(path, **kwargs)

    def __call__(self):
        return self.app

