from flask import Flask, request, jsonify, abort
import socket
import json
import sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)


host = '127.0.0.1'
port = 5050

app = Flask(__name__)
def get_answer_from_engine(bottype,query):
    mySocket = socket.socket()
    mySocket.connect((host,port))
    json_data = {
        "Query" : query,
        "BotType":bottype
    }
    #챗봇엔진에 먼저 받은 jsonformat 보내고
    message = json.dumps(json_data)
    #print(message)
    mySocket.send(message.encode())

    # 챗봇엔진 답변 출력
    data = mySocket.recv(2048).decode()
    ret_data = json.loads(data)
    mySocket.close()
    #print("ret_data:",ret_data)
    return ret_data



@app.route('/', methods=['GET'])
def index():
    return 'hello', 200


# 챗봇 엔진 query 전송 API
@app.route('/query/<bot_type>', methods=['POST'])
def query(bot_type):
    body = request.get_json()
    try:
        if bot_type == 'TEST':
            # 챗봇 API 테스트
            ret = get_answer_from_engine(bottype=bot_type, query=body['query'])
            return jsonify(ret)

        elif bot_type == "KAKAO":
            # 카카오톡 스킬 처리
            body = request.get_json()
            utterance = body["userRequest"]["utterance"]
            ret = get_answer_from_engine(bottype=bot_type,query = utterance)
            from jbot_api.KakaoTemplate import KakaoTemplate
            #위 코드 되는것 확인
            skillTemplate = KakaoTemplate()
            return skillTemplate.send_response(ret) 
        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 오류
        abort(500) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)