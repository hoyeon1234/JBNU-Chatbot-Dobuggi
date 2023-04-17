import pandas as pd
import datetime as dt
import sys,os,re
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
import threading
import json
#PathConfig()

class JbotLogging():
    
    def __init__(self,log_directory):
        """
        Input
        log_directory : 로그가 입력될 폴더이름
        """
        self.log_directory = log_directory

    def get_path(self):
        """
        로그를 저장할 경로를 만들어주는 함수
        self.logpath에 경로가 저장되도록 함.

        input : x
        output : x
        """
        x = dt.datetime.now()
        date = str(x.date())
        file_ext = ".csv"
        file_name = date + file_ext
        log_path = os.path.join(self.log_directory,file_name)
        log_path = log_path.replace("\\","/")
        return log_path
    def create_log(self,json_data):
        """
        챗봇스킬서버의 응답을 받아서 로그를 기록해주는 함수.
        Input
        json_dict : 챗봇 스킬서버에서 카카오 봇 시스템에 보내는 json의 딕셔너리 파일
        Output x
        """
        #저장경로 얻기
        log_path = self.get_path()
        #print(log_path)
        #time 정보 작성
        x = dt.datetime.now()
        hour = x.hour;minute=x.minute;second = x.second
        time = str(hour)+":"+str(minute)+":"+str(second)
        #print(time)
        #작성할 로그 만들기
        txt_log = ""
        for _,value in json_data.items():
            #로그저장할때에는 한글만 기록
            try:
                value = re.sub("[^A-Za-z0-9가-힣]"," ",value) #\n을 기록해놓으면 엑셀안에서 여러줄에 걸쳐서 기록하는 오류 포착 
            except: #None일 경우 re.sub오류 발생하므로 예외처리
                pass
            #답변이 잘 되는지만 확인하므로 \n제거
            if value is not None:
                txt_log += value+","
            else:
                txt_log += ","
        txt_log = time+","+txt_log[:-1]+"\n"
        #print(txt_log)
        if not os.path.exists(log_path):
            with open(log_path,"w") as f: #write mode
                header = "time,query,answer,AnswerImageUrl,intent,ner_tag,timepoint,day,detailloc\n"
                f.write(header)
                f.write(txt_log)
        else:
            with open(log_path,'a') as f: #addmode
                f.write(txt_log)