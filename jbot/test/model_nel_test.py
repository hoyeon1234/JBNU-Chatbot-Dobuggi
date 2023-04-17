import sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
from jbot.models.ner.NerModel import NerModel
PathConfig()


ner = NerModel(ner_mapping_data = ner_final)

sent = "사범대 어딘지 알려줘유~"
d = ner.predict(sent,"위치")
print(d)

sent = "인문대 어디야?"
d = ner.predict(sent,"위치",True)

sent = "공대위치"
d = ner.predict(sent,"위치",True)

sent = "위치 상대 어디?"
d = ner.predict(sent,"위치",True)

sent = "it응용 과사어디야?"
d = ner.predict(sent,"학과사무실",True)
print(d)

sent = "it정보 과사 어디야?"
d = ner.predict(sent,"학과사무실",True)
print(d)

sent = "컴공 과사 어디야?"
d = ner.predict(sent,"학과사무실",True)
print(d)

sent = "독일학과 과사 어디야?"
d = ner.predict(sent,"학과사무실",True)
print(d)

sent = "총학생회 인스타"
d = ner.predict(sent,"sns안내",True)
print(d)

sent = "참빛 언제까지 열어?"
d = ner.predict(sent,"교내식당 운영시간",True)
print(d)

sent = "기시공 과사"
d = ner.predict(sent,"학과사무실",True)
print(d)

sent = "진수원"
d = ner.predict(sent,"교내식당 운영시간",True)
print(d)