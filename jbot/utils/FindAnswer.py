import sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
from jbot.utils.Database import Database
from jbot.models.ner.NerModel import NerModel
from jbot.models.intent.IntentModel import IntentModel
from jbot.models.sub.Toolbox import Toolbox
import random
import re
import numpy as np
"""
교내학식은 붙여서 !
교내(띄고)공지 교내 공지는 띄어서!
"""


class FindAnswer():
    """
    db에서 답변을 검색하기 위한 객체
    """
    def __init__(
        self,db,intent_model,ner_model,tbx):
        """
        Input 
        db : Database 객체
        intent_model : 의도분류 모델 객체
        ner_model : 개체명 인식 모델 객체
        tbx : 툴박스 객체
        """
        self.db = db
        self.intent_model = intent_model
        self.ner_model = ner_model
        self.tbx = tbx

    def get_values(self,query,printing = False):
        """
        의도를 받아서 적절한 의도 + (개체명,시점,날짜,세부위치) 정보(information)를 반환
        Input : intent_name(string,의도)
        Output
        intent_name이 "위치" 일 경우
        [의도,개체명] 반환
        intent_name이 "교내학식"일 경우
        [의도,개체명,시점,날짜,세부위치] 정보를 반환
        ...
        """
        #소문자로 변환
        try:
            query = query.lower()
        except:
            pass
        #1. 의도분류
        intent = self.intent_model.predict_class(query)

        #2. 분류된 의도에 따른 적절한 값 가져오기
        if intent == "위치":
            _ner_tag = self.ner_model.predict(query,intent)
            _detailloc = self.tbx.get_detailloc(query)
            _timepoint = None
            _day = None
        elif intent == "교내학식":
            _ner_tag = self.ner_model.predict(query,intent)
            if _ner_tag == "새빛관" or _ner_tag == "한빛관" or _ner_tag == "대동관" or _ner_tag == "평화관":
                _ner_tag = "직영관" #새빛,한빛,대동,평화의 경우 "직영관"에서 밥 먹으므로 직영관데이터로 통일
            _detailloc = None
            _timepoint = self.tbx.get_timepoint(query)
            if _ner_tag == "후생관" :
                _timepoint = "전체"
            _day = self.tbx.get_day(query)
        elif intent == "교내 공지": #교내공지는 교내(한칸띄고) 공지임 ... ㅜㅜ... 오류발생하니까 조심
            #교내공지의 경우 ner,timepoint,day,detailloc가 모두 없음
            _ner_tag = None 
            _timepoint = None
            _detailloc = None
            _day = None
        elif intent == "학과사무실":
            #의도가 학과사무실인 경우 _ner_tag는 어떤학과사무실인지 알려주는 ner임
            _ner_tag = self.ner_model.predict(query,intent) 
            _timepoint = None
            _detailloc = None
            _day = None
        elif intent == "sns안내":
            #의도가 SNS안내인 경우 _ner_tag는 어떤 단체의 SNS인지 알려주는 ner
            _ner_tag = self.ner_model.predict(query,intent)
            if _ner_tag is None:
                _ner_tag = "전체"
            _timepoint = None
            _detailloc = None
            _day = None
        elif intent =="교내식당 운영시간":
            _ner_tag = self.ner_model.predict(query,intent)
            if _ner_tag == "새빛관" or _ner_tag == "한빛관" or _ner_tag == "대동관" or _ner_tag == "평화관":
                _ner_tag = "생활관 직영관 운영시간" #새빛,한빛,대동,평화의 경우 "직영관"에서 밥 먹으므로 직영관데이터로 통일
            elif _ner_tag == "진수원":
                _ner_tag = "진수원 운영시간"
            elif _ner_tag == "후생관":
                _ner_tag = "후생관 운영시간"
            elif _ner_tag == "참빛관":
                _ner_tag = "생활관 참빛관 운영시간"
            _timepoint = None
            _detailloc = None
            _day = None

        information = [intent,_ner_tag,_timepoint,_day,_detailloc]
        if printing == True:
            print("query",query)
            print("intent",intent)
            print("informa",information)
        return information
        
    def _make_query(self,inform):
        """
        mysql의 db에서 데이터를 가져오기 위한 쿼리문(sql구문) 만들기
        intent_name,ner_tags,timepoint,day,detailloc 총 4가지의 값을 받아서 db의 row를 가져오는 sql구문 생성

        case 1. intent_name = "교내학식" 인 경우
        1. ner_final(개체명 인식을 위한 데이터)에서 의도가 "교내학식"인 경우의 유의어만 가져와서 개체명과 매핑하여 어떤 식당인지 파악 ㅇ
        2. timepoint에서 유의어들을 가져와서 아침,점심,저녁? 분류 => toolbox객체에서 아침,점심,저녁? 유의어 인식하고 매핑하는 함수 만들기 ㅇ
        3. day에서 유의어들을 가져와서 요일 분류 => day에서 유의어들을 가져와서 요일 분류 ㅇ
        4. 어떤식당(ner),시점(timepoint),요일(day)정보를 바탕으로 db에서 데이터 검색하고 가져오기 

        case2. intent_name = "위치" 인 경우
        1. ner_final(개체명)에서 의도가 "위치"인 경우의 유의어만 가져와서 개체명과 매핑하여 어떤 건물인지 파악 ㅇ
        2. 문장내에서 숫자를 탐지하여 몇호관을 물어보는지 파악(호관이없을수도 있음.그때는 null값 리턴) ㅇ
        3. 건물정보,호관정보를 바탕으로 db에서 데이터 검색하고 가져오기 ㅇ

        case3. intent_name = "교내공지"인 경우
        1. 교내공지의 answer인 링크를 가져오기(일단은 링크로 ... 추후에 ) ㅇ

        case4. intent_naem = "학과사무실"인 경우
        1. ner_final(개체명)에서 의도가 "학과사무실"인 경우의 유의어만 가져와서 개체명과 매핑하여 어떤 학과사무실에 대한 정보를 묻는지 파악 
        2. 어떤학과사무실(ner)인지 정보를 바탕으로 db에서 데이터 검색하고 가져오기
        """
        sql = "select * from jbot_train_data " #where을 다음에 붙여줘야 하기에 반드시 한칸 띄운다
        intent = inform[0];_ner_tag = inform[1];_timepoint = inform[2];_day= inform[3];_detailloc = inform[4] 

        
        #1. 의도가 "위치" 인 경우
        if intent == "위치" and _ner_tag is not None and _detailloc is not None:
            sql += "where ner = '%s' " % _ner_tag
            sql += "and detailloc = '%s' " % _detailloc
            sql += "and intent = '%s' " % intent
        elif intent == "위치" and _ner_tag is not None:
            sql += "where ner = '%s' " % _ner_tag
            sql += "and intent = '%s' " % intent
        
        elif intent == "위치": #질문의 의도가 위치를 물어보는 것만 아는 경우 (장소는 정확하게 입력되지 않은 경우)
            sql = None
        
        #2. 의도가 "교내학식"인 경우
        #intent,_ner_tag,_timepoint,_day 정보 활용
        #_timepoint는 없는 경우가 없음. 입력이 없다면 정의된 시간구간안에서 하나의 시점으로 가정 => 따라서 timepoint가 Null에 대한 분기는 없음
        #_day는 없는 경우가 없음. 입력이 없다면 오늘정보로 가정 => 따라서 day가 Null에 대한 분기는 없음

        if intent =="교내학식" and _ner_tag is not None: #어떤 식당인지 인지한 경우
            sql += "where intent = '%s' " % intent
            sql += "and ner = '%s' " % _ner_tag
            sql += "and timepoint = '%s' " % _timepoint
            sql += "and day = '%s' " % _day
        elif intent =="교내학식" and _ner_tag is None: #어떤 식당인지 인지못한 경우
            #print("어떤 식당인지 자세히 알려주세요 ㅜㅜ")
            sql = None
        
        #3. 의도가 "교내 공지"인 경우

        if intent == "교내 공지" : #교내공지를 묻는 발화가 입력된 경우 
            sql += "where intent = '%s' " % intent

        #4. 의도가 "학과사무실"인 경우
        #intent,_ner_tag(과사무실 이름정보) 활용
        if intent == "학과사무실" and _ner_tag is not None:
            sql += "where intent = '%s' " % intent
            sql += "and ner = '%s' " % _ner_tag
        elif intent == "학과사무실":
            sql = None
        
        #5. 의도가 "sns안내"인 경우
        #intent,_ner_tag(단체 이름정보) 활용
        if intent == "sns안내" and _ner_tag is not None:
            sql += "where intent = '%s' " % intent
            sql += "and ner = '%s' " % _ner_tag
        elif intent == "sns안내" and _ner_tag is None:
            sql += "where intent = '%s' " % intent
            sql += "and ner = '%s' " % _ner_tag

        #6. 의도가 "교내식당 운영시간"인 경우
        if intent == "교내식당 운영시간" and _ner_tag is not None:            
            sql += "where intent = '%s' " % intent
            sql += "and ner = '%s' " % _ner_tag
        elif intent == "교내식당 운영시간":
            sql = None        

        #print(sql)
        return sql
    def search(self,query):
        """
        Input
        query

        Output 
        (answer(답변),answer_image(답변이미지)) (if db에 데이터가 존재할 경우)
        (None,None) (if db에 데이터가 없을 경우)
        """
        #print("search진입")
        #답변을 검색할 정보 만들기
        inform = self.get_values(query)
        #print(f'search의 information : {inform}')

        #검색한 정보로부터 sql구문 만들기
        sql = self._make_query(inform)
        #print(f'search의 sql : {sql}')
        #print(f'sql : {sql}')
        if sql is None:
            print("db에서 답변을 검색하지 못했습니다.")
            return (None,None)

        #connection객체를 만들고 db와 연결
        self.db.connect() 

        """
        print("가져온 데이터 체크")
        for data in answer:
            print(answer["answer"],answer["answer_image"])
        """
        #db에서 검색된 모든 정보 가져오기
        try:
            answer = self.db.select_one(sql)
            self.db.close()
            return (answer['answer'], answer['answer_image'])
        except:
            nodata_text = "가지고 있는 데이터가 없어요..\n"
            if inform[0] == "교내학식":
                nodata_text += "아마도 열지않았거나 없는 장소인 것 같아요(o ╹‿ ╹ o)"
            self.db.close()
            return (nodata_text,None)

        
        #print(answer)
        #db와 연결해제
        #answer에서 답변 1개만 가져오는 구문 order by rand limit 1구문 일단 생략
    def answering(self,query):
        
        #길이가 너무 짧을 경우 좀 더 길게 말해달라 하는 부분,근데 필요없어서 제외
        #print("answering함수 진입")
        """
        try:
            test_query = re.sub(" ","",query)
        except:
            pass
        tooshort = ["조금 더 자세히 말씀해 주실래요?（￣ー￣）","조금 더 길게 말씀해 주실래요?¯\(ºдಠ)/¯","너무 짧아요 ... 자세히 좀 ... ≧(´▽｀)≦"]
        if len(test_query) <=2:
            text = random.sample(tooshort,1)[0]
            return (text,None)
        #print("tooshort처리 완료")
        """
        confusion = ["Σ(‘◉⌓◉’) 무슨 말인지 잘 모르겠어요. ","이해하기가 힘들어요..(°ヘ°) ","너무 어려워요.. へ[ ᴼ ▃ ᴼ ]_/¯ ",
        "아직 공부를 별로 안했어요 (๑′°︿°๑) ","한국어 너무 어려워요 (;*△*;) "]
        requirmore = ["조금 더 자세히 입력해주세요!!(￣◇￣;)","조금만 더 쉽게 말해주세요(°◇°;)","말씀 좀 자세히... 좀 ... 부탁드립니다⎝⎛♥‿♥⎞⎠","더 자세히 말씀해주실 수 있나요?꒰ •⸝⸝⸝⸝⸝⸝⸝• ꒱"]
    
        #print("getvale함수 진입")
        #inform으로부터 문장의 정보 파악
        inform = self.get_values(query) #쿼리(질문)에서 정보를 추출한 infrom을 가져옴
        intent = inform[0];_ner_tag = inform[1];_timepoint = inform[2];_day= inform[3];_detailloc = inform[4] 

        #print("확률계산 진입")
        yhat = self.intent_model.yhat
        if np.max(yhat) <= 0.5:
            text = random.sample(confusion,1)[0] + random.sample(requirmore,1)[0]
            return (text,None)
        
        
        #1.위치일 경우
        if intent == "위치" and _ner_tag is not None: #건물까지 인식한경우
            return self.search(query)
        elif intent == "위치" and _ner_tag is None: #건물인지 인식못한경우
            text = random.sample(confusion,1)[0] +"어떤 위치를 찾고있나요? 조금 더 자세히 입력해주세요...ヾ(≧▽≦*)"
            return (text,None)
        
        #2.교내학식
        if intent == "교내학식" and _ner_tag is not None: #식당인식한경우
            return self.search(query)
        elif intent =="교내학식" and _ner_tag is None: #식당인식못한경우
            text = random.sample(confusion,1)[0] +"혹시 학식을 찾고계신가요? 어떤 식당인지도 알려주실래요?⸜(｡˃ ᵕ ˂ )⸝"
            return (text,None)

        
        #3.교내공지
        공지단어유형 = ["입학","학기","모집","전형","신입생","전기","후기","연계과정","합격자","법학","수시","정시","발표","요강","일정","추가모집",
        "원서접수","장학생","근로","국가장학","장학재단","한국장학재단","학자금","장학금","학자금대출","근로봉사","취업","면접","채용",
        "설명회","작성법","상반기","하반기","해외취업","기업","벨트","박람회","수학","신청","계절학기","계절수업","학사교류 ","학점교류",
        "연계","수강신청","학점","교직","교과목","대학원","큰사람","사업단","협력","평화통일","개최","국제","토론","통일교육","창업","프로그램",
        "교육","강좌","언어교육부","언어","집중","외국어","센터","캠프","세부","심사","안내","진로","봉사","특강","참여자","모집","일정","접수",
        "안내","공지","공고","선발","공모","홍보","교내공지","공지","ㄱㅈ","사항","공지사항","교내 공지","ㄱㄴㄱㅈ","ㄱㅈㅅㅎ"]

        if intent == "교내 공지": 
            #교내공지이면서 공지단어키워드를 가지고있으면 교내공지관련 데이터 가져오도록 수정(왜냐면 ... 너무 교내공지 위주로 판별했음)
            for word in 공지단어유형:
                if word in query:
                    return self.search(query) 
            #교내공지이면서 공지단어키워드를 안가지고있으면 혼란스러운 메세지 출력
            text = random.sample(confusion,1)[0] + random.sample(requirmore,1)[0] 
            return (text,None)
    


        #4.학과사무실
        if intent =="학과사무실" and _ner_tag is not None: #어떤 학과의 사무실인지 인지한 경우
            return self.search(query)
        elif intent == "학과사무실":
            text = random.sample(confusion,1)[0] +"혹시 학과사무실 정보를 찾으시나요? 조금 더 자세히 입력해주세요.٩(◕ᗜ◕)و"
            return (text,None)

        
        #5. SNS안내
        if intent == "sns안내" and _ner_tag is not None:
            return self.search(query)
        elif intent == "sns안내":
            text = random.sample(confusion,1)[0] +"혹시 SNS를 검색하시나요? 조금 더 자세히 입력해주세요...๏_๏"
            return (text,None)

        if intent == "교내식당 운영시간" and _ner_tag is not None:
            return self.search(query)
        elif intent == "교내식당 운영시간":
            text = random.sample(confusion,1)[0] + '혹시 식당 운영시간을 검색하시나요? 어떤 식당인지도 알려주실래요?╭( •̀ •́ )╮'
            return (text,None)