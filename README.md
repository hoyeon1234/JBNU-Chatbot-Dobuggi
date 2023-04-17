# dobbuggi
lstm 기반 전북대학교 챗봇 도북이 입니다!<br>
학식,과사무실위치,건물위치,공지사항 등의 서비스를 제공합니다.

# Project Goal
- `딥러닝`과목에서 수강한 RNN,LSTM,GRU 아키텍쳐 활용
- DB에서 배포까지 하나의 서비스를 관통하는 모든 프로세스 수행 
- local 서버 만들어 보기.

# stack 
- python
- mysql

# Results
![](./results/department.png)<br>
![](./results/position.png)<br>
![](./results/rice.png)<br>

# 보완할 점 & 아쉬운 점
- LSTM으로 텍스트를 먼저 분류하고 정해진 답변을 매핑하는 구조이기에 자율성이 한정됨
- 학습데이터가 충분하지 못했기에 저조한 인식률
    - 더 충분한 문장 데이터를 확보해야 함.
