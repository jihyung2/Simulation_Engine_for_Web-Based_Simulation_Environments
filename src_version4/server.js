const express = require("express");
const path = require("path");
const fs = require("fs");
const app = express();
const port = 3000;

// express-ws 가져오기
const expressWs = require("express-ws")(app);

async function main() {
  const { default: fetch } = await import("node-fetch");

  // 정적 파일 등록
  app.use(express.static("public"));

  // 메인 페이지
  app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public/templates", "index.html"));
  });

  // 웹소켓 경로 설정
  app.ws("/ws", (ws, req) => {
    // 클라이언트가 연결되면 로그 출력
    console.log("Client connected");

    ws.on("close", () => {
      console.log("Client disconnected");
    });
  });

  // 웹훅 처리
 app.post("/start_simulation", express.json(), async (req, res) => {
  const data = req.body;
  const username = req.params.username;
  const port = req.params.port;
  console.log("시뮬레이션 구성 데이터:", data);
  const options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  };

  const url = "http://127.0.0.1:8900/start_simulation";

  try {
    const response = await fetch(url, options);
    const result = await response.json();
    console.log(result);

    // 연결된 모든 클라이언트에게 데이터를 전송
    expressWs.getWss().clients.forEach((client) => {
      client.send(JSON.stringify(result));
    });

    // 수정: 결과를 반환하는 부분을 제거
  } catch (error) {
    console.error("Error:", error);
    res.status(500).send("Error: " + error.message); // 오류 메시지 반환
    return; // 에러 시에 반환을 종료
  }

  const newData = { ...data, username, port };

  expressWs.getWss().clients.forEach((client) => {
    client.send(JSON.stringify(newData));
  });

  res.json(newData); // 결과를 반환하도록 변경
});

  app.post("/:username", express.json(), async (req, res) => {
  const data = req.body;
  const username = req.params.username;
  const port = req.params.port;
  console.log("웹훅 데이터:", data);

  // 클라이언트에게 전송할 새로운 객체 만들기
  const newData = { ...data, username, port };

  // 연결된 모든 클라이언트에게 데이터를 전송
  expressWs.getWss().clients.forEach((client) => {
    client.send(JSON.stringify(newData));
  });

  res.status(200).send("웹훅 데이터가 정상적으로 처리되었습니다.");
});

  // 웹 서버 실행
  app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
  });
}
main();