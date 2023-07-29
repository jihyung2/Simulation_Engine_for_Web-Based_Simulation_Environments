# Simulation_Engine_for_Web-Based_Simulation_Environments


### 에러

시뮬레이션에서 웹훅으로 데이터를 전송하는 문제가 있었음

비동기로 안하면 시뮬레이션이 무한으로 동작하기때문에 블로킹되어 실행이 되지않음

비동기로 하면 output이나 int_trans에 async를 붙여야하는데 이걸 붙이면 pyevsim에 전체 코드를 고쳐야하는 문제가 발생했음

시뮬레이션 결과만 출력하는거라면 문제가 없지만 중간에 데이터를 게속 받아오는 역할로 사용했기 때문에 저기 사이에 넣어야됨

## Thread를 사용해서 문제를 해결했다. 
