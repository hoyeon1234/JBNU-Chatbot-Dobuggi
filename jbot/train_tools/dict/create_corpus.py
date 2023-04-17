#raw_data로부터 corpus를 만드는 모듈
import os,sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
import pandas as pd
import numpy as np
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess

################################################
def create_corpus_data():
    df1 = pd.read_excel(raw_chatbot_train_path1)
    df2 = pd.read_excel(raw_chatbot_train_path2)
    df3 = pd.read_csv(raw_chatbot_train_path3)
    df4 = pd.read_excel(raw_chatbot_train_path4)
    df5 = pd.read_csv(raw_chatbot_train_path5)
    df6 = pd.read_excel(raw_chatbot_train_path6)

    #_df = pd.concat([df1,df2,df3,df4,df5],axis=0)[["질문","의도"]]
    _df = pd.concat([df1,df2,df3,df4,df5,df6],axis=0)[["질문","의도"]]
    print(_df)
    print("널 값을 지우기전 :",len(_df))
    
    queries,intents = [],[]
    for obs in _df.itertuples():
        query,intent =obs[1],obs[2]
        intents.append(intent)
        try:
            if query.isupper():
                queries.append(query.lower())
            else:
                queries.append(query)
        except:
            queries.append(query)
            #print("질문",query)
            #print("의도",intent)
    _df["질문"] = queries;_df["의도"] = intents
    
    _df = _df.dropna(axis=0).reset_index(drop=True)
    lower_intent = []
    for intent in _df["의도"]:
        if intent.isupper():
            lower_intent.append(intent.lower())
        else:
            lower_intent.append(intent)
    _df["의도"] = lower_intent
    print("널 값을 지운 후 :",len(_df))
    print("최종 데이터의 길이 :",len(_df))
    return _df
_df = create_corpus_data()

_df["의도"].value_counts()
_df.to_excel(corpus_path)

"""
upper_sum = 0
for _,obs in _df.iterrows():
    query = obs["질문"]
    if query.isupper():
        upper_sum+=1
upper_sum
"""