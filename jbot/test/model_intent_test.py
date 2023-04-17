import sys
import pymysql
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
from jbot.models.intent.IntentModel import IntentModel
PathConfig()

p = Preprocess(word2index_dic = chatbot_dict_path,user_dic = user_dic_path)
intent_model = IntentModel(model_name=intent_model_path,intent_mapping = intent_mapping_path,preprocess = p)

_query = "후생관 내일 점심 메뉴 뭐나와"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

#교내 공지
_query = "공지사항"
intent_model.predict_class(_query,printing = True)

_query = "공지보여줘"
intent_model.predict_class(_query,printing = True)


_query = "공지사항 알려줘~"
intent_model.predict_class(_query,printing = True)

_query = "공지"
intent_model.predict_class(_query,printing = True)

_query = "교내 공지사항 알려줄래?"
intent_model.predict_class(_query,printing = True)

_query = "도북아 공지사항"
intent_model.predict_class(_query,printing = True)

_query = "공지뭐있노"
intent_model.predict_class(_query,printing = True)


#교내학식
_query = "오늘 참빛ㅊ관 식당 저녁 메뉴 좀 알려줘"
intent_model.predict_class(_query,printing = True)

_query = "오늘메뉴"
intent_model.predict_class(_query,printing = True)

query = "오늘 대동관 밥"
intent_model.predict_class(_query,printing = True)

_query = "대동관 저녁밥"
intent_model.predict_class(_query,printing = True)

_query = "밥뭐야?"
intent_model.predict_class(_query,printing = True)

_query = "저녁"
intent_model.predict_class(_query,printing = True)

_query = "점심"
intent_model.predict_class(_query,printing = True)


_query = "아침"
intent_model.predict_class(_query,printing = True)

#위치
_query = "공대 1호관 위치"
intent_model.predict_class(_query,printing = True)

_query = "인문대 ㅇㄷ"
intent_model.predict_class(_query,printing = True)


#과사무실 정보
_query = "심리학과  번호"
intent_model.predict_class(_query,printing = True)

_query = "It응용 과사 번호"
intent_model.predict_class(_query,printing = True)

_query = "경영학과 과사무실 위치랑 번호좀 알려줄래?"
intent_model.predict_class(_query,printing = True)

_query = "전자공 과사 위치"
intent_model.predict_class(_query,printing=True)

#총학생회 인스타
_query = "총학생회 인스타 들어가줘"
intent_model.predict_class(_query,printing = True)

_query = "총동연 "
intent_model.predict_class(_query,printing = True)

_query = "전북대학교 인스타 "
intent_model.predict_class(_query,printing = True)

_query = "인스타"
intent_model.predict_class(_query,printing = True)


_query = "하위 도북아"
intent_model.predict_class(_query,printing = True)

_query = "시발럼아"
intent_model.predict_class(_query,printing = True)

_query = "무야호"
intent_model.predict_class(_query,printing = True)

_query = "하윙 ^^"
intent_model.predict_class(_query,printing = True)

_query = "도북씨"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "의대식당"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "오늘 의대식당 한식"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "후생관"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "후생관 학식"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "후생관 시간"
intent_model.predict_class(_query,printing = True)
intent_model.yhat


_query = "중도 편의점"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "편의점 운영시간"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "편의점 몇시까지야?"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "편의점"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "sns 뭐있어"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "후생관 언제까지 운영해"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "학교식당 몇시까지얌?"
intent_model.predict_class(_query,printing = True)
intent_model.yhat


_query = "도북아"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "공지사항"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "진수원"
intent_model.predict_class(_query,printing = True)
intent_model.yhat


_query = "서로만 바라보다 언젠가 우리~~"
intent_model.predict_class(_query,printing = True)
intent_model.yhat

_query = "기숙사 위치"
intent_model.predict_class(_query,printing = True)
intent_model.yhat