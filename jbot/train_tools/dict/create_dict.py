#corpus로부터 lookuptable을 만드는 모듈
#즉,단어 - 정수 매핑관계를 만드는 모듈
import os,sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
import pandas as pd
import numpy as np
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle
#PathConfig()

def create_dict():
    """
    corpus에 있는 모든 문서에 대해서 토큰화를 하여 고유한 단어의 집합인 딕셔너리(Vocab,사전)을 만들어주는 함수
    Input : X
    Output : dictionary(고유한 단어의 집합)
    """
    p = Preprocess(user_dic = user_dic_path)
    corpus_data = pd.read_excel(corpus_path)
    corpus_data = corpus_data.drop(columns = [corpus_data.columns[0]]) 
    corpus = corpus_data.질문 #질문,의도(레이블)가 같이 있는 데이터에서 질문분리하여 말뭉치를 만듦
    dict = []
    for i in corpus:
        pos = p.pos(i)
        tokens = p.get_keywords(pos,without_tag = True)
        for token in tokens:
            if token not in dict:
                dict.append(token)

    return dict
    
dict = create_dict()
print(f'corpus에 존재하는 중복되지 않는 단어의 총 수: {len(dict)}')
dict
def create_mapping():
    """
    단어-정수 매핑 즉 ,lookup table 또는 word2index를 만들어서 경로에 저장하는 함수
    Input : X
    Output : 경로에 저장된 바이너리 단어-정수 매핑 파일
    """
    tokenizer = preprocessing.text.Tokenizer(oov_token = "OOV") #정수매핑을 만들어주는 케라스의 Tokenizer객체 만듦
    tokenizer.fit_on_texts(dict) #정수매핑 만들기,tokenizer.word_index에 저장되어 있음
    word_index = tokenizer.word_index
    print(len(word_index))
    f = open(chatbot_dict_path,"wb")
    try:
        pickle.dump(word_index,f)
    except Exception as e:
        print(e)
    finally:
        f.close()
create_mapping()