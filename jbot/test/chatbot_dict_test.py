#단어사전 테스트 모듈
import os,sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
import pickle
PathConfig()
f = open(chatbot_dict_path,"rb")
word_index = pickle.load(f)
f.close()

sent = "공지 ㅊㅇ버지원과 뭐 있어?"
p = Preprocess(user_dic = user_dic_path,word2index_dic = chatbot_dict_path)
_t = p.preprocess(sent,printing=True)
print(f'입력문장 : {sent}')
print(f"전처리된 문장 : {_t}")

sent = "공지 ㅊㅇ버지원과 뭐 dasgda 있어?"
p = Preprocess(user_dic = user_dic_path,word2index_dic = chatbot_dict_path)
_t = p.preprocess(sent,printing=True)
print(f'입력문장 : {sent}')
print(f"전처리된 문장 : {_t}")

sent = "hi hello hoyeon good"
p = Preprocess(user_dic = user_dic_path,word2index_dic = chatbot_dict_path)
_t = p.preprocess(sent,printing=True)
print(f'입력문장 : {sent}')
print(f"전처리된 문장 : {_t}")
