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
from jbot.utils.FindAnswer import FindAnswer


db = Database(host = DB_HOST,user = DB_USER,db_name = DB_NAME,password = DB_PASSWORD)
p = Preprocess(word2index_dic = chatbot_dict_path,user_dic = user_dic_path)
intent = IntentModel(model_name = intent_model_path,intent_mapping = intent_mapping_path,preprocess = p)
ner = NerModel(ner_final)
tbx = Toolbox(ner_final)


#교내공지
f = FindAnswer(db,intent,ner,tbx)
sent = "장학금 관련 공지 "
d = f.answering(sent)
print(d)

sent = "장학금 공지사항 "
d = f.answering(sent,True)
print(d)


#학과사무실
sent = "it응용 과사무실 번호"
d = f.answering(sent)
print(d)

sent = "기계공학부 학과사무실 정보"
d = f.answering(sent)
print(d)

sent = "과사무실 정보"
d = f.answering(sent)
print(d)


#위치
sent = "상과대학 1호관 위치"
d = f.answering(sent)
print(d)

sent = "인문대 1호관 위치"
d = f.answering(sent)
print(d)

sent = "인문대 위치"
d = f.answering(sent)
print(d)

sent = "위치 알려줘"
d = f.answering(sent)
print(d)


#장소 시점 요일정보 모두 있는 경우
sent = "오늘 참빛관 밥 뭐나와?"
#g = f.get_values(sent)
d = f.answering(sent)
print(d)

sent = "새빛 금요일 저녁은 뭐야?"
#g = f.get_values(sent)
d = f.answering(sent)
print(d)

#장소만 모두 있는 경우
sent = "새빛관 밥 메뉴"
#g = f.get_values(sent)
d = f.answering(sent)
print(d)

sent = "기숙사 밥"
#g = f.get_values(sent)
d = f.answering(sent)
print(d)

sent = "긱사 밥 뭐나옴?"
d = f.answering(sent)
print(d)

sent = "후생관 내일 점심 메뉴 뭐나와"
d = f.answering(sent)
print(d)

#교내식당 운영시간

sent = "밥뭐노"
d = f.answering(sent)
print(d)

sent = "대동관 운영시간이 언제까지야"
d = f.answering(sent)
print(d)
d

sent = "하위 도북아"
d = f.answering(sent)
print(d)
d

sent = "시발럼아"
d = f.answering(sent)
print(d)
d

sent = "무야호"
d = f.answering(sent)
print(d)


sent = "하윙 ^^"
d = f.answering(sent)
print(d)

sent = "도북씨"
d = f.answering(sent)
print(d)


sent = "얍마"
d = f.answering(sent)
print(d)