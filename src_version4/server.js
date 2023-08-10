const express = require("express");
const path = require("path");
const fs = require("fs");
const app = express();
const port = 3000;
async function main() {
  const { default: fetch } = await import("node-fetch");

  // 정적 파일 등록
  app.use(express.static("public"));

  // 메인 페이지
  app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public/templates", "index.html"));
  });

  // 웹훅 처리
  app.post("/start_simulation", express.json(), async (req, res) => {
    const data = req.body;
    console.log("웹훅 데이터:", data);
    const options = {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data),
    };

    const url = "http://127.0.0.1:8900/start_simulation";

    try {
      const response = await fetch(url, options);
      const result = await response.json();
      console.log(result);
      res.json(result); // 결과를 반환하도록 변경
    } catch (error) {
      console.error("Error:", error);
      res.status(500).send("Error: " + error.message); // 오류 메시지 반환
    }
  });

  // 웹 서버 실행
  app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
  });
}
main()