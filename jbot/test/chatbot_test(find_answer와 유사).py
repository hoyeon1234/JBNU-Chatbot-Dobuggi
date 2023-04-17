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


db = Database(
    host = DB_HOST,user = DB_USER,password = DB_PASSWORD,db_name = DB_NAME
)
p = Preprocess(word2index_dic = chatbot_dict_path,user_dic = user_dic_path)
intent = IntentModel(model_name = intent_model_path,intent_mapping = intent_mapping_path,preprocess = p)
ner = NerModel(ner_mapping_data = ner_final)
tbx = Toolbox(ner_final)

try :
    f = FindAnswer(db,intent,ner,tbx)
    db.connect()
    sent = "상과대학 1호관 위치"
    d = f.search(sent)
    print(d)
    #g = f.get_values(sent)

    #장소 시점 요일정보 모두 있는 경우
    sent = "참빛관 금 저녁"
    d = f.search(sent)
    print(d)

    sent = "새빛 금요일 저녁은 뭐야?"
    d = f.search(sent)
    print(d)

    #장소만 모두 있는 경우
    sent = "새빛 밥"
    d = f.search(sent)
    print(d)

    sent = "한빛밥"
    d = f.search(sent)
    print(d)

    sent = "내일 메뉴"
    d = f.search(sent)
    print(d)

    sent = "직영관 금요일 저녁은 뭐야?" #왜 오류뜨냐? 아직 교내 공지관련 구문이 완성이 안되었기 때문! => 완성하고 다시... ㄱㄱ
    d = f.search(sent)
    print(d)

    sent = "오늘 한빛 아침 밥?"
    d = f.search(sent)
    print(d)
except:
    answer = "죄송해요 , 무슨말인지 모르겠어요 ㅜㅜ"
    print(answer)
finally:
    db.close()
    print("db연결해제")