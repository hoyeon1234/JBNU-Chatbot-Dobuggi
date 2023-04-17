import pandas as pd
import datetime as dt
import sys,os
import numpy as np
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
from jbot.utils.BotServer import BotServer
from jbot.utils.Database import Database
from jbot.models.ner.NerModel import NerModel
from jbot.models.intent.IntentModel import IntentModel
from jbot.models.sub.Toolbox import Toolbox
from jbot.utils.FindAnswer import FindAnswer
from jbot.utils.JbotLogging import JbotLogging
import threading
import json



p = Preprocess(word2index_dic = chatbot_dict_path,user_dic = user_dic_path)
intent = IntentModel(model_name = intent_model_path,intent_mapping = intent_mapping_path,preprocess = p)
ner = NerModel(ner_mapping_data = ner_final)
tbx = Toolbox(ner_final)
jbotlogging = JbotLogging(jbotlog_directory_path)
def to_client(conn,addr,params):
    db = params["db"] #params의 키값 db에 Database의 객체가 저장되어 있음

    try:
        db.connect() #DB객체로 서버와 연결

        # 데이터 수신
        read = conn.recv(2048) #수신 데이터가 있을 때 까지 블로킹
        #print("===========================")
        print("Connection from %s" % str(addr))

        if read is None or not read:
            #클라이언트 연결이 끊어지거나 오류가 있는 경우
            print("클라이언트 연결 끊어짐")
            exit(0)
        
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ",recv_json_data)
        query = recv_json_data["Query"]

        
        try:
            f = FindAnswer(db,intent,ner,tbx)
            #의도파악,개체명,시점,요일,세부장소 파악
            inform = f.get_values(query,True)
            for i in range(len(inform)):
                if inform[i] is None:
                    inform[i] = "인식하지못함"
            
            intent_name = inform[0];_ner_tag = inform[1];_timepoint = inform[2];_day= inform[3];_detailloc = inform[4] 
            answer,answer_image = f.answering(query)
            print(answer,answer_image)
            #sql + 답 출력
        except:
            answer = "알 수 없는 오류가 발생했어요.. (￣▽￣)ノ\n(화면캡쳐후 전송부탁드려요!! 2266880@naver.com)"
            intent_name = _ner_tag = _timepoint = _day = _detailloc = answer_image = None
        
        send_json_data_str = {
            "Query" : query,
            "Answer" : answer,
            "AnswerImageUrl" : answer_image,
            "Intent" : intent_name,
            "ner_tag" : _ner_tag,
            "timepoint" : _timepoint,
            "day" : _day,
            "detailloc" : _detailloc
        }
        print(send_json_data_str)
        #로그저장
        #혹시 오류가 발생할 수 있으므로 예외처리
        try:
            jbotlogging.create_log(send_json_data_str)
            #print(send_json_data_str)
            print("로그 저장 완료")
        except:
            print("로그저장 오류 발생")
            pass
        
        #message = json.dumps(send_json_data_str)
        message = json.dumps(send_json_data_str,ensure_ascii=False) #이렇게 해야 한글 인코딩이 잘됨
        conn.send(message.encode())
        print("응답 전송 완료")
        print("===========================" * 4)


    except Exception as ex:
        print(ex)
    finally:
        if db is not None:
            db.close()
        conn.close()

if __name__ == "__main__":
    # 질문/답변 학습 디비 연결 객체 생성
    db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
    )
    print("DB 접속")

    port = 5050
    listen = 100

    # 봇 서버 동작
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start")

    while True:
        conn, addr = bot.ready_for_client()
        params = {
            "db": db
        }

        client = threading.Thread(target=to_client, args=(
            conn,
            addr,
            params
        ))
        client.start()