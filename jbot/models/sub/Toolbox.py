import sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
from jbot.models.ner.NerModel import NerModel
from jbot.models.intent.IntentModel import IntentModel
from tensorflow.keras.models import load_model
import pandas as pd
#PathConfig()
import time
import re
import datetime as dt
import random

class Toolbox():
    def __init__(self,ner_mapping_data):
        self.data = pd.read_excel(ner_mapping_data).drop(columns = "Unnamed: 0")
    def get_detailloc(self,query):
        """
        입력된 문장(query)로부터 세부위치 즉 몇호관인지를 알려주는 함수
        Input : query(string)
        Output : 호관정보(string) or None(숫자가 10이 넘어갈 경우 10호관부터는 없는 호관이기에 None을 출력)
        """
        num = re.sub("[^0-9]","",query)
        #print(type(num))
        if num != "" and int(num)<10:
            return num+"호관"
        else:
            #print("호관정보는 없습니다.")
            return None
        #if num == "":
    def get_day(self,query):
        """
        입력된 문장(query)로부터 몇요일인지 알려주는 함수
        Input : query(string)
        Output : 요일(string) 월요일,화요일,수요일...금요일,토요일,일요일
        """
        day_mapping = {0:"월요일", 1:"화요일", 2:"수요일", 3:"목요일", 4:"금요일", 5:"토요일", 6:"일요일"}
        synonym_tomorrow= ["내일","ㄴㅇ"]
        synonym_today = ["오늘","ㅇㄴ"]
        day_synonym = {"월요일":["월요일","월"],"화요일":["화요일"],"수요일":["수요일"],"목요일":["목요일","목"],"금요일":["금요일","금"],"토요일":["토요일","토"],"일요일":["일요일"]} 
        #"일"을 추가하면 ..일요일,월요일,화요일 전부인식
        #"수"를 추가하면 진수원 검색시 무조건 수요일로 인식
        #"화"를 추가하면 평화관 검색시 무조건 화요일로 인식
        #대동,평화,참빛,진수,후생
        
        #"내일"의 유의어들이 문장에 포함되어 있으면 내일이 몇요일인지 반환
        for synn in synonym_tomorrow:
            if synn in query:
                x = dt.datetime.now()
                mapping_num = x.weekday() + 1
                if mapping_num == 7:
                    mapping_num = 1
                answer = day_mapping[mapping_num]
                return answer

        #"오늘"의 유의어들이 문장에 포함되어 있으면 오늘이 몇요일인지 반환
        for synn in synonym_today:
            if synn in query:
                x = dt.datetime.now()
                answer = day_mapping[x.weekday()]
                return answer

        #각각의 요일의 유의어들이 문장에 포함되어 있을때 요일을 반환
        for day,day_synn in day_synonym.items():
            for synn in day_synn:
                if synn in query:
                    return day
        #아무경우도 아니라면 .... 오늘의 요일 반환
        return day_mapping[dt.datetime.now().weekday()]

    def get_timepoint(self,query):
        """
        입력된 문장(query)로부터 시점을 알려주는 함수
        Input : query(string)
        Output : 시점(string) 즉, 아침 or 점심 or 저녁  or None(입력된 문장에서 시점이 없는 경우)
        """
        #교내학식 유의어 중 시점과 관련있는 유의어 데이터만 가져옴
        #시점과 관련있는 유의어는 개체명에 "관"이라는 글자가 없음(아침,점심,저녁만 있기 떄문에)
        condition = (self.data["의도"] == "교내학식") & ((self.data["개체명"] == "아침") | (self.data["개체명"] == "점심") | (self.data["개체명"] == "저녁"))
        synonym_df = self.data.loc[condition,:]
        #print(synonym_df)

        #문장내에 시점찾기
        tps = []
        for row_num,row_data in synonym_df.iterrows():
            if row_data["유의어"] in query:
                tps.append(row_data["개체명"])
        #print("찾은 시점 목록 :",tps)
        #문장내에서 시점관련 유의어가 있으면
        if len(tps) > 0:
            answer = random.sample(tps,1)[0] #ㅈㅅ의 경우 유의어가 "조식"과 "점심"의 유의어 이므로 둘 중 랜덤으로 하나 반환
            return answer
        #문장내에 시점관련 유의어가 없으면 ?
        #현재 시간을 기준으로 파악!
        else:
            x = dt.datetime.now()
            if 0<=x.hour<=10:
                return "아침"
            elif 10<x.hour<=16:
                return "점심"
            elif 16<x.hour<=24:
                return "저녁"





"""
tbx = Toolbox(ner_mapping_data=ner_final)

sent = "오늘 참빛관 밥 뭐야?"
d = tbx.get_timepoint(sent)
print(d)

sent = "내일 참빛관 점심 뭐야?"
tbx.get_timepoint(sent)

sent = "내일 참빛관 ㅈㅅ 뭐야?"
tbx.get_timepoint(sent)

sent = "내일 후생점심 뭐야?"
tbx.get_timepoint(sent)
"""

"""
sent = "내일 참빛관 아침 뭐야?"
day = tbx.get_day(sent)
print(day)

sent = "오늘 참빛관 아침 뭐야?"
day = tbx.get_day(sent)
print(day)

sent = "참빛관 아침 뭐야"
day = tbx.get_day(sent)
print(day)
"""

"""
tbx = Toolbox()
p = Preprocess(word2index_dic = chatbot_dict_path,user_dic = user_dic_path)
intent = IntentModel(model_name = intent_model_path,intent_mapping = intent_mapping_path,preprocess = p)
ner = NerModel(ner_final)

#PathConfig()
sent = "공대13호관 ㅇㄷ?"
intent_name = intent.predict_class(sent)
print(intent_name)
ner_tag = ner.predict(sent)
print(ner_tag)
detailloc = tbx.get_detailloc(sent)
print(detailloc)

sent = "공대5호관 ㅇㄷ?"
intent_name = intent.predict_class(sent)
print(intent_name)
ner_tag = ner.predict(sent)
print(ner_tag)
detailloc = tbx.get_detailloc(sent)
print(detailloc)
"""