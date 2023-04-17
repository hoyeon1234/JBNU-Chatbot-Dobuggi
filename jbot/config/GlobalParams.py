#단어사전 테스트 모듈
import sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.PathConfig import *
from jbot.utils.Preprocess import Preprocess
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
MAX_SEQ_LEN = 12 #새로운데이터 들어보면 밑에 구문 실행시키고 다시 업데이트
"""
최대 문장길이 확인 코드
def get_max_sequence():
    df = pd.read_excel(corpus_path);df = df.drop(columns = df.columns[0])
    p = Preprocess(user_dic=user_dic_path,word2index_dic=chatbot_dict_path)
    queries = df["질문"]

    len_queries = []
    for query in queries:
        try:
            len_queries.append(len(p.preprocess(query)))
        except:
            pass
    return max(len_queries)
MAX_SEQ_LEN = get_max_sequence()
print(f'MAX_SEQ_LEN =',MAX_SEQ_LEN)
"""