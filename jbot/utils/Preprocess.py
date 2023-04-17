import sys
import re
import pickle
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from konlpy.tag import Komoran
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
#PathConfig()
"""
전처리모듈
1. 토큰화,정제
2. 벡터화
3. 임베딩
"""
class Preprocess:
    def __init__(self,word2index_dic = None,user_dic = None):
        """
        Preprocess 클래스의 인스턴스(객체)를 만들때 실행되는 생성자
        Input
        word2index_dic (단어-정수매핑 바이너리파일,chatbot_dict_path입력)
        user_dic (사용자 정의 단어사전)
        Output 
        X
        """
        #토큰화기능이 있는 Komoran객체 생성
        self.komoran = Komoran(userdic = user_dic)
        #미리 불용어들 정의
        self.exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC','SF', 'SP', 'SS', 'SE', 'SO','EP', 'EF', 
            'EC', 'ETN', 'ETM','XSN', 'XSV', 'XSA','null'
        ]
        if word2index_dic is not None:
            f = open(word2index_dic,"rb")
            self.word_index = pickle.load(f)
            f.close()
        else:
            print("word2index_dic의 경로를 입력해주세요")
            self.word_index = None
    def pos(self,sentence):
        """
        문장내에 있는 품사(part of speech,pos)들을 파악하여 단어,품사쌍 목록을 반환해주는 함수
        Input : sentence
        Output : list[("word1","POS1"),("word2","POS2")...]
        """
        #sentence = re.sub("[^0-9ㄱ-ㅣ가-힣]",' ',sentence)
        if sentence.isupper():
            sentence = sentence.lower()
        _temp = re.sub("[^0-9ㄱ-ㅣ가-힣a-zA-Z]"," ",sentence)
        return self.komoran.pos(_temp)
    def get_keywords(self,pos,without_tag = False):
        """
        단어-품사리스트에서 불용어에 해당하는 품사를 제외한 단어를 가져옴
        Input : list[("word1","POS2"),("word2","POS2")]
        Output : [word1,word2,...,] (without_tag = True)
        """
        word_pos = pos #단어와 품사가 태깅된 튜플인데 pos라고 하는건
        #뭔가 직관적이지 못해서 나는 word_pos로 변수명지어줄꺼임
        word_list = []
        for pair in word_pos:
            #print(pair)
            word,pos = pair
            #print("hihihi")
            #print(word,pos)
            if without_tag == False and pos not in self.exclusion_tags:
                word_list.append((word,pos))
            elif without_tag == True and pos not in self.exclusion_tags:
                word_list.append(word)
            else:
                pass
        return word_list
    def except_stopwords(self,pos,without_tag = False):
        """
        get_keywords와 동일한 함수(연습했던 코드와 이름을 같게하기 위해사용)
        단어-품사리스트에서 불용어에 해당하는 품사를 제외한 단어를 가져옴
        Input : list[("word1","POS2"),("word2","POS2")]
        Output : [word1,word2,...,] (without_tag = True)
        """
        return self.get_keywords(pos=pos,without_tag=without_tag)
    def preprocess(self,sentence,printing = False):
        """
        토큰화 + 정제 + 벡터회까지 전처리 과정을 한번에 수행해주는 함수
        Input : setence(str)
        Output : [word1,word2,...,] (without_tag = True)
        """
        without_tag = True
        keywords = self.get_keywords(self.pos(sentence=sentence),without_tag=without_tag) #정제,토큰화까지 진행
        if printing == True:
            print("tokenization + cleaning 후 남은 단어(토큰)들",keywords)
        answer = self.get_wordidx_sequence(keywords)
        if printing == True:
            print("정수인코딩",answer)
        return answer
    def get_wordidx_sequence(self,keywords):
        if self.word_index is None:
            print("word2index_dic의 경로를 입력해주세요")
            return []
        w2i = []
        for word in keywords:
            try:
                wd_idx = self.word_index[word]
                w2i.append(wd_idx)
            except:
                w2i.append(self.word_index["OOV"])
        return w2i


"""
#test_code

sent = "ㄱㄷdfalk 1호관 위치 dgk"
p = Preprocess(user_dic=user_dic_path,word2index_dic = chatbot_dict_path)
pos = p.pos(sent)
print(pos)
keywds=p.get_keywords(pos,True)
print(keywds)
_t = p.get_wordidx_sequence(keywds)
print(_t)
#문제 : 호관을 인식 못함

sent = "교내 멘토링 공지사항 뭐 있어?"
p = Preprocess(user_dic=user_dic_path,word2index_dic = chatbot_dict_path)
#help(Preprocess.__init__)
pos = p.pos(sent)
print(pos)
keywds=p.get_keywords(pos,True)
print(keywds)
_t = p.get_wordidx_sequence(keywds)
print(_t)

sent = "후생관 오늘 저녁밥 뭐나옴?"
p = Preprocess(user_dic=user_dic_path,word2index_dic = chatbot_dict_path)
pos = p.pos(sent)
print(pos)
keywds=p.get_keywords(pos,True)
print(keywds)
_t = p.get_wordidx_sequence(keywds)
print(_t)
"""