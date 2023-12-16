# Simulation_Engine_for_Web-Based_Simulation_Environments

**팀 구성** 
- 한밭대학교 20187098 이지형

## <u>Teamate</u> Project Background
- ### 필요성
  - 모델링 및 시뮬레이션은 사회과학 및 공학 분야 뿐 아니라 사회 전반의 여러 분야에서 정의된 문제를 해결되는데 활용되고 있음
  - 이러한 모델링 및 시뮬레이션을 활용한 문제 해결에 있어 중요한 것은 문제를 정의하고, 컴퓨터 시뮬레이션을 수행할 수 있도록 모델을 개발하고 실행하는 것
- ### 문제점  
  - 상용 시뮬레이션 환경을 구축하기 위해서 별도의 어플리케이션을 구매하고 설치해야 하는 문제점이 존재
  - 모델링 및 시뮬레이션에 대한 지식 외에 실행 환경에 대한 추가적인 지식이 필요하다는 점에서 모델링 및 시뮬레이션 적용을 저해하는 문제점이 존재
  - 이러한 요소들은 많은 사용자가 모델링 및 시뮬레이션을 손쉽게 활용할 수 있도록 하는 접근성 측면에서 제약사항으로 존재함
- ### 해결책
  - 모델링 및 시뮬레이션의 사용자 접근성을 향상시키기 위한 방안으로, 커맨드 라인 인터페이스 기반 시뮬레이션 환경을 제안함
  - 제안하는 시스템은 이산사건 시스템 형식론 기반으로 구현된 모델을 조합하여 시뮬레이션을 구성하고 실행할 수 있도록 함으로써 별도의 어플리케이션을 설치하고 실행하는 제약사항을 극복
  
## System Design
  - ### System Requirements
    - 모델링 및 시뮬레이션에 대한 지식외 실행 환경에 대한 지식없이 시뮬레이션 사용
    - 시뮬레이션 환경 구축을 위한 별도의 추가비용 제거
    - 많은 사용자가 모델링 및 시뮬레이션을 손쉽게 사용할 수 있도록 접근성 향상

  - ### System Architecture
  ![작동방식](https://github.com/jihyung2/Simulation_Engine_for_Web-Based_Simulation_Environments/assets/108830942/89703dee-746d-49d3-8ba5-ce7d49a535ea)

  
## 💻 Tech Stack
<h4> Platforms & Languages </h4>

<div align="left">
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
    <img src="https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white">
    <img src="https://img.shields.io/badge/fastapi-002512?style=for-the-badge&logo=fastapi&logoColor=white">
    <img src="https://img.shields.io/badge/javascript-654812?style=for-the-badge&logo=javascript&logoColor=white">
</div>

<h4> Tools </h4>
<div align=left>
	<img src="https://img.shields.io/badge/Intellij%20IDE-000000?style=flat&logo=intellijidea&logoColor=white" />
	<img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/>
    <img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=white"/>
	<img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=GitHub&logoColor=white" />
</div>
  
## Conclusion
  - 웹 기반 시뮬레이션 인터페이스와 시뮬레이션 엔진은 이산사건 시스템 형식론 기반으로 구현된 모델을 조합하여 시뮬레이션을 구성하고 실행할 수 있도록 함으로써, 별도의 어플리케이션을 설치하고 실행하는 환경적 제약사항 극복
  
## Project Outcome
- ### 2023년 한국전기전자학회 학술대회 논문
![웹 기반 시뮬레이션 환경을 위한 시뮬레이션 엔진의 설계 및 구현_이지형논문001](https://github.com/jihyung2/Simulation_Engine_for_Web-Based_Simulation_Environments/assets/108830942/c3243f1b-5a1e-41f6-9aed-529be301564c)
![웹 기반 시뮬레이션 환경을 위한 시뮬레이션 엔진의 설계 및 구현_이지형논문002](https://github.com/jihyung2/Simulation_Engine_for_Web-Based_Simulation_Environments/assets/108830942/f45867d2-d10b-411c-ba47-c7852f0e203c)

- ### 2023년 한국전기전자학회 포스터 발표
![1_pan](https://github.com/jihyung2/sat_simulation/assets/108830942/ea5a71c3-ff9e-4113-a9f9-f633c5c1ac7a)

- ### 2023년 한국전기전자학회 참가확인서
![2_pan2](https://github.com/jihyung2/sat_simulation/assets/108830942/ec43f03f-7b0b-4265-824a-ee46344a45a9)

- ### 동작 과정
     ![작동방식2](https://github.com/jihyung2/Simulation_Engine_for_Web-Based_Simulation_Environments/assets/108830942/0ed6dad7-12a7-4f98-8589-7f524f94a50e)
    - 사용자가 시뮬레이션 구성정보를 입력 후 실행 버튼을 클릭하면 웹 서버가 구성 정보를 실행 서버로 전달
    - 실행 서버는 전달받은 시뮬레이션 구성정보를 바탕으로 독립적인 시뮬레이션 모델을 생성 후 실행
    - 시뮬레이션 동작 중 이벤트 발생시 웹 훅을 통해 웹 서버로 데이터 전달

- ### 실행 화면
  ![실행화면](https://github.com/jihyung2/Simulation_Engine_for_Web-Based_Simulation_Environments/assets/108830942/a2e65d98-db28-49d7-a5bf-d47e6eb2fd51)


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
   
   

