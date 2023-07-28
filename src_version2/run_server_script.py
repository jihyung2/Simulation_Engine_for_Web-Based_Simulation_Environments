import subprocess
import time

server_script = "main.py"

while True:
    print("서버를 갱신합니다.")

    # 서버를 중단하고 스크립트를 실행 (Windows에서는 taskkill 사용)
    subprocess.run(["taskkill", "/F", "/T", "/IM", "uvicorn.exe"])
    subprocess.run(["python", server_script])

    print("서버가 종료되었습니다. 10초 후에 다시 실행합니다.")
    time.sleep(10)
