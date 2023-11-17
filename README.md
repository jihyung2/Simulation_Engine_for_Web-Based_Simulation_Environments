# Simulation_Engine_for_Web-Based_Simulation_Environments

**팀 구성** 
- 한밭대학교 20187098 이지형

## <u>Teamate</u> Project Background
- ### 필요성
  - 학습에 어려움이 있는 학생들에게 개인별 맞춤형 학습 서비스를 제공함으로써 학습능력 향상
  - 학생이 원하면 언제든 시공간의 제약을 받지 않고 부족한 부분을 도움 받을 수 있도록 챗봇을 개발하여 학습 적응 지원
- ### 기존 해결책의 문제점
  - 기존의 프로그래밍 언어 관련 수업에서는 학생 개개인의 역량과 이해도 차이로 인해 편차가 크게 발생하는 문제가 존재
  - 학생들을 지도할 때 1:1로 살피고 개별 피드백을 해주는 것이 중요하지만 현실적으로 어려움 이러한 문제를 해결하기위해 챗봇 개발을 목표로함
  
## System Design
  - ### System Requirements
    - 사용자가 챗봇에 파이썬 이론에 관한 질문을 하면 답변된 Q&A 데이터에서 적절한 답변을 추출 후 답변 
    - 모바일, 웹 환경 모두 챗봇 환경 지원
    - 파이썬 코딩 실습 환경 제공을 위한 온라인 저지 구축

  - ### System Architecture
  
  
## 💻 Tech Stack
<h4> Platforms & Languages </h4>

<div align="left">
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
    <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
    <img src="https://img.shields.io/badge/fastapi-000000?style=for-the-badge&logo=fastapi&logoColor=white">
	
</div>

<h4> Tools </h4>
<div align=left>
	<img src="https://img.shields.io/badge/Intellij%20IDE-000000?style=flat&logo=intellijidea&logoColor=white" />
	<img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/>
    <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/>
	<img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=GitHub&logoColor=white" />
</div>
  
## Conclusion
  - 논문에서 긁어오기
  
## Project Outcome
- ### 2023년 한국전기전자학회 학술대회

- ### 실제 작동사진




## 개발과정

### 에러
시뮬레이션에서 웹훅으로 데이터를 전송하는 문제가 있었음
비동기로 안하면 시뮬레이션이 무한으로 동작하기때문에 블로킹되어 실행이 되지않음
비동기로 하면 output이나 int_trans에 async를 붙여야하는데 이걸 붙이면 pyevsim에 전체 코드를 고쳐야하는 문제가 발생했음
시뮬레이션 결과만 출력하는거라면 문제가 없지만 중간에 데이터를 게속 받아오는 역할로 사용했기 때문에 저기 사이에 넣어야됨
--> Thread를 사용해서 문제를 해결했다. 

### 에러2 
하지만 문제가 웹훅을 동기로 전송하면 블로킹으로 막혀서 시뮬레이션이 멈춰야 한번에 들어가졌다.
이러한 문제를 해결하려고 오랜시간 삽질을 했지만 고칠 수 없었고 웹훅을 비동기로 바꾸면 pyevsim에 전체 코드를 고쳐야하는 문제가 있고
새로운 루프를 만드려고 했으나 이미 루프(시뮬레이션 동작)가 존재하여 그것 어려워보였다.
그래서 비동기로 써야만 블로킹이 되지 않기때문에 고민을 해보았다
1. 웹훅을 동기로 사용 -> 시뮬레이션이 정상 동작하나, 블로킹으로 시뮬레이션이 종료되어야 한번에 전송
2. 웹훅을 비동기로 사용 -> 시뮬레이션을 실행할때 1번 출력 외에 게속 동작하는 코드 안에 넣으면 pyevsim 전체를 수정해야하는 에러가 발생
---> 웹훅을 무조건 비동기로 해야하고 시뮬레이션을 실행했을때나 시간제한을 줘서 종료했을때만 실행할 수 있기 때문에 시뮬레이션을 1초씩 무한번 실행하게 함

### 에러3
웹훅 방식으로 바로 웹페이지로 전달하는것에서 막혔음
그래서 1차 모델로 html에서 get result로 수신된 웹훅 데이터를 받는 내용으로 일단 수정함

### 기본 구현 초안 -완-
1. 드롭박스형태의 독립적인 시뮬레이션 모델 만들기 ex) A,B,C,D중 체크, port, name 수집 (add 여러개 가능) 후 run ( 입력된 여러 정보들로 각각의 시뮬레이션 작동 (멀티 프로세싱))
2. 웹훅( 시뮬레이션 이벤트가 발생했을때 웹훅으로 데이터 전송 )

### 개선안
여러 버전으로 개발하면서 version4에서 최종으로 마무리가 되었다.
웹훅을 비동기로 실행시키기 위해서는 두가지 방법이 있었음
1. 시뮬레이션 엔진을 비동기로 전환한다 -> 이 방법은 오픈소스 pyevsim 전체를 비동기로 수정해야해야 하므로 사실상 불가능이였다. 
2. 멀티프로세스로 시뮬레이션 실행하기 -> 이 방법으로 해결했다.
구글링하여 많은 방법을 사용해봤으나( 멀티 쓰레딩 등등 ) 결국 안에서 블로킹 당하는건 피할수없었기 때문에 실행 자체를 멀티 프로세싱으로 하는 방법만이 유일했는데, 결국 성공해서 최종본을 완성할 수 있었다.

### 최종본 완성
웹 기반 시뮬레이션 엔진은 시뮬레이션 구성을 설정할 수 있는 웹 서버와 시뮬레이션 구성 정보를 받아 시뮬레이션 모델을 구성하고 실행하는 실행 서버로 구성된다.
기존에 실행 서버에서 경유하는 방식으로 했지만, 웹 서버(node.js)와 실행서버(fast api)로 확실히 분리한 후 완성했다.

#### 작동과정
웹 서버에서 시뮬레이션 구성정보를 실행서버에게 전달한다.
실행서버가 구성정보를 받아 시뮬레이션을 돌린다.
시뮬레이션이 멀티프로세싱으로 동작하면서 이벤트가 발생하면 웹훅으로 데이터를 웹 서버에게 전송한다.
웹 서버는 node.js로 데이터를 받아서 html과 웹 소켓으로 연결하여 실시간으로 받은 데이터를 웹 프론트로 실시간 출력한다.

#### Node.js 환경 세팅
1. Node.js 공식 웹사이트에서 Node.js를 설치한다.
2. cmd나 터미널에서 프로젝트 파일로 이동한후 npm init -y 입력
3. npm install express path 입력
4. npm install node-fetch 입력
   
   

