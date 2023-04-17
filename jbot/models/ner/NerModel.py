import sys
import pymysql
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
import pandas as pd
import time
class NerModel():
    def __init__(self,ner_mapping_data):
        self.data = pd.read_excel(ner_mapping_data).drop(columns = "Unnamed: 0")
    def predict(self,query,intent,printing = False):
        """
        질문(쿼리)와 의도 입력받아서 검색된 개체명 반환.
        매핑이 될 단어들을 print해주는 기능도 존재
        Input : query(string,문장),분류된 의도(string)
        Output : ner(string,) => 매핑된 장소가 있으면 매핑된 장소중 첫 번째 장소를 없으면 None을 반환
        """
        condition = self.data["의도"] == intent
        intent_df = self.data.loc[condition,:]
        #print(intent_df)

        #비직관적인코드 .. 나중에 수정
        #교내학식과 관련된 유의어는 시점 그리고 장소명과 관련된 유의어가 있음
        #이 중 여기서는 시점과 관련된 유의어는 판단하는 것이 아니므로 "관"이 포함된 장소명과 관련된 유의어데이터만 활용
        #장소명과 관련된 유의어만 포함하지 않을 경우,원래 데이터에는 시점과 관련된 데이터가 포함되어 있으므로 잘못된 결과 도출
        if intent == "교내학식":
            """
            cond = (intent_df["개체명"] == "대동관" | intent_df["개체명"] == "평화관" | intent_df["개체명"] == "참빛관" | intent_df["개체명"] == "새빛관" | intent_df["개체명"] == "한빛관" | intent_df["개체명"] == "창의관"\
                | intent_df["개체명"] == "진수원" | intent_df["개체명"] == "후생관")
            """
            cond = ((intent_df["의도"] == "교내학식") & ~(intent_df["개체명"] == "아침") & ~(intent_df["개체명"] == "점심") & ~(intent_df["개체명"] == "저녁"))
            ner_df = intent_df.loc[cond,:]
        else:
            ner_df = intent_df

        n = len(ner_df)
        mapped_ner = []
        for_print = []
        for i in range(n):
            obs = ner_df.iloc[i,:]
            ner = obs["개체명"]
            synonym = obs["유의어"]
            if synonym in query and ner not in mapped_ner:
                mapped_ner.append(ner)
                if printing == True:
                    for_print.append((ner,synonym))
        if printing == True:
            print("질문:",query)
            print("인식된 개체명:",for_print)
        try : 
            return mapped_ner[0] #만
        except :
            return None