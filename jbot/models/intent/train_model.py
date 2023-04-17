#의도분류모델링 모듈
import sys
import pickle
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
from jbot.config.GlobalParams import *
from jbot.utils.Preprocess import Preprocess
import pandas as pd 
import numpy as np
from tensorflow.keras import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding,Dense,Dropout,Bidirectional,LSTM,Flatten,SpatialDropout1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
#!pip install keras-self-attention
from keras_self_attention import SeqSelfAttention
import tensorflow as tf
from sklearn.model_selection import train_test_split
#import tensorflow_addons as tfa

#데이터읽어오기
df = pd.read_excel(corpus_path);df = df.drop(columns = df.columns[0])
df
#의도정수매핑 만들기
intent_mapping = {}
idx = 0
for intent in df["의도"]:
    if intent not in intent_mapping.keys():
        intent_mapping[intent] = idx
        idx+=1
intent_mapping #의도에 널값이 있는 경우는 ... 데이터를 받아오면서 intent변수가 없는 경우가 있었기 떄문임. 반드시 체크!
#질문,의도 분류해서 리스트 만들기

#의도분류 매핑 저장
f = open(intent_mapping_path,"wb")
try:
    pickle.dump(intent_mapping,f)
except Exception as e:
    print(e)
finally:
    f.close()

queries = np.array(df["질문"].tolist())
#intents = np.array([intent_mapping[query] for query in df["의도"]]).reshape(-1,1)
intents = np.array([intent_mapping[query] for query in df["의도"]])

queries.shape,intents.shape

print(f'질문 갯수 : {len(queries)}')
print(f'의도 갯수 : {len(intents)}')
#전처리된 텍스트 데이터 생성(시퀀스 데이터 생성)
sequences = []
p = Preprocess(user_dic = user_dic_path,word2index_dic = chatbot_dict_path)
for query in queries:
    sequence = p.preprocess(query)
    sequences.append(sequence)
#남은전처리하나 - 제로패딩 하기
padded_seqs = preprocessing.sequence.pad_sequences(sequences,maxlen = MAX_SEQ_LEN,padding = 'post')
padded_seqs
#전처리완료 - 정제,토큰화,벡터화

#train/valid/test split
train_size = int(len(padded_seqs) * 0.7)
val_size = int(len(padded_seqs) * 0.2)
test_size = int(len(padded_seqs) * 0.1)

train_idx,test_idx = train_test_split(range(len(padded_seqs)),test_size=test_size,random_state = 10,shuffle = True,stratify = intents)
test_X = padded_seqs[test_idx]
test_y = intents[test_idx]
print(f'test_X : {test_X.shape},tets_y : {test_y.shape}')
traindata_X = padded_seqs[train_idx]
traindata_y = intents[train_idx]
train_idx,valid_idx = train_test_split(range(len(traindata_X)),test_size = val_size,random_state = 10,shuffle = True,stratify=traindata_y)
train_X = traindata_X[train_idx]
train_y = traindata_y[train_idx]
val_X = traindata_X[valid_idx]
val_y = traindata_y[valid_idx]
print(f'train_X : {train_X.shape},tets_y : {train_y.shape}')
print(f'val_X : {val_X.shape},val_y : {val_y.shape}')
print("label ratio ===========================================")
print(f'test\n{pd.Series(test_y).value_counts()/len(test_y)}')
print(f'train\n{pd.Series(train_y).value_counts()/len(train_y)}')
print(f'val\n{pd.Series(val_y).value_counts()/len(val_y)}')
#ds = tf.data.Dataset.from_tensor_slices((padded_seqs,intents))
train_X.shape,train_y.shape
test_ds = tf.data.Dataset.from_tensor_slices((test_X,test_y)).batch(20)
valid_ds = tf.data.Dataset.from_tensor_slices((val_X,val_y)).batch(20)
train_ds = tf.data.Dataset.from_tensor_slices((train_X,train_y)).batch(20)


#Setting Hyperparameter
dropout_prob = 0.5
emb_size = 32
vocab_size = len(p.word_index) + 1
num_classes = len(intent_mapping)
MAX_SEQ_LEN #(벡터화를 시킨 후 이미 최대문장길이에 맞춤)
#f1 = tfa.metrics.F1Score(num_classes = num_classes,average = None)
from keras.callbacks import EarlyStopping
es = EarlyStopping(monitor = "val_loss",mode = 'min',patience=10)

#model
model = Sequential()
model.add(Embedding(vocab_size, emb_size, mask_zero=True))
model.add(SpatialDropout1D(0.8))
model.add(LSTM(40))
model.add(Dropout(0.8))
model.add(Dense(64, activation='relu', kernel_regularizer = regularizers.l2(0.01)))
model.add(Dense(num_classes,activation = "softmax"))
model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(0.0001), metrics=["accuracy"])
model.summary()
model.fit(train_ds,validation_data = valid_ds,epochs =300,verbose = 1,callbacks = [es])

model.evaluate(test_ds,verbose=1)

model.save(intent_model_path)