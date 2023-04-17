import sys
import pymysql
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
import tensorflow as tf
from tensorflow.keras.models import Model,load_model
from tensorflow.keras import preprocessing
import pickle
import numpy as np


#의도분류모델모듈
class IntentModel:
    def __init__(self,model_name,intent_mapping,preprocess):
        """
        의도분류모델 객체
        Input
        model_name : intent_model_path
        intent_mapping : intent_mapping(의도-정수 매핑정보,레이블 매핑)
        p : Preprocess 객체
        """
        with open(intent_mapping,"rb") as f :
            self.labels = pickle.load(f)#label2index
        
        self.index2label = self.reverse_dict(self.labels) #index2label
        self.model = load_model(model_name) 
        self.p = preprocess
        self.yhat = None
    def predict_class(self,query,printing=False,record_predict = True):
        """
        클라이언트로부터 질문을 받으면 의도를 예측하는 함수
        Input : 한국어 텍스트(질문,쿼리)
        Output : 예측된 의도(한국어 출력)
        """
        #전처리(패딩제외)-토큰화,벡터화(정수인코딩)
        sequences = [self.p.preprocess(query)] #왜 한번 더 리스트로 감싸? => iterable한 오브젝트여야 함(`sequences` must be a list of iterables. Found non-iterable: 9)
        #print(sequences)
        #전처리 - 패딩처리   
        from jbot.config.GlobalParams import MAX_SEQ_LEN
        padded_seqs = preprocessing.sequence.pad_sequences(sequences,maxlen = MAX_SEQ_LEN,padding = "post")
        #print(padded_seqs)
        predict = self.model.predict(padded_seqs)
        #print(predict)
        predict_class = tf.math.argmax(predict,axis=1).numpy()[0]
        if printing == True:
            #print(f'입력된문장 : {query}')
            print(f'전처리된문장 : {padded_seqs}')
            print(f'모델의 출력결과 : {np.round(predict,2)}')
            print(f'예측된 의도 : {self.index2label[predict_class]}')
        if record_predict == True:
            self.yhat = np.round(predict,2)
        return self.index2label[predict_class]
    def reverse_dict(self,dict):
        """
        반대로매핑해주는 함수
        """
        answer = {}
        for key,value in dict.items():
            answer[value] = key
        return answer




"""
#ckcode
p = Preprocess(word2index_dic = chatbot_dict_path,user_dic = user_dic_path)
#help(p.preprocess)
_model = IntentModel(model_name=intent_model_path,intent_mapping = intent_mapping_path,preprocess = p)
_model.labels
_model.index2label
_model.model
_model.p
sent = "화요일 후생관 메뉴"
_t = _model.predict_class(sent,True)
_t
"""