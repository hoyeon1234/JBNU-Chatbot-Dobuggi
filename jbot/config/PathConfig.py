#혜선,희정,한별로부터 받은 데이터로부터 챗봇 학습데이터 경로
raw_chatbot_train_path1 = "C:/Users/22668/Desktop/jbot/train_tools/qna/교내학식.xlsx" 
raw_chatbot_train_path2 = "C:/Users/22668/Desktop/jbot/train_tools/qna/교내공지.xlsx" 
raw_chatbot_train_path3 = "C:/Users/22668/Desktop/jbot/train_tools/qna/위치.csv" 
raw_chatbot_train_path4 = "C:/Users/22668/Desktop/jbot/train_tools/qna/sns.xlsx" 
raw_chatbot_train_path5 = "C:/Users/22668/Desktop/jbot/train_tools/qna/과사무실.csv" 
raw_chatbot_train_path6 = "C:/Users/22668/Desktop/jbot/train_tools/qna/교내식당 운영시간.xlsx" 

train_file = "C:/Users/22668/Desktop/jbot/train_tools/qna/train_data.xlsx"
user_dic_path = "C:/Users/22668/Desktop/jbot/utils/jbot_dict.tsv"
corpus_path = "C:/Users/22668/Desktop/jbot/train_tools/dict/corpus.xlsx"
chatbot_dict_path = "C:/Users/22668/Desktop/jbot/train_tools/dict/chatbot_dict.bin"
intent_model_path = "C:/Users/22668/Desktop/jbot/models/intent/intent_model.h5"
intent_mapping_path = "C:/Users/22668/Desktop/jbot/models/intent/intent_mapping.bin"
ner_data_path1 = "C:/Users/22668/Desktop/jbot/train_tools/nerdata/교내학식 유의어.xlsx"
ner_data_path2 = "C:/Users/22668/Desktop/jbot/train_tools/nerdata/교내공지 유의어.csv"
ner_data_path3 = "C:/Users/22668/Desktop/jbot/train_tools/nerdata/위치 유의어.xlsx"
ner_data_path4 = "C:/Users/22668/Desktop/jbot/train_tools/nerdata/sns 유의어.xlsx"
ner_data_path5 = "C:/Users/22668/Desktop/jbot/train_tools/nerdata/과사무실 유의어.xlsx"
ner_data_path6 = "C:/Users/22668/Desktop/jbot/train_tools/nerdata/교내학식 운영시간 유의어.xlsx"

ner_final = "C:/Users/22668/Desktop/jbot/train_tools/nerdata/유의어final.xlsx"
timepoint_model_path = "C:/Users/22668/Desktop/jbot/models/sub/timepoint.h5"
jbotlog_directory_path = "C:/Users/22668/Desktop/jbot/train_tools/chatlog"


def PathConfig():
    global raw_chatbot_train_path1,raw_chatbot_train_path2,raw_chatbot_train_path3
    print(f'raw_chatbot_train_path1 = {raw_chatbot_train_path1}')
    print(f'raw_chatbot_train_path2 =  {raw_chatbot_train_path2}')
    print(f'raw_chatbot_train_path3 = {raw_chatbot_train_path3}')
    print(f'raw_chatbot_train_path4 = {raw_chatbot_train_path4}')
    print(f'raw_chatbot_train_path5 = {raw_chatbot_train_path5}')
    print(f'raw_chatbot_train_path6 = {raw_chatbot_train_path6}')

    print(f'train_file = {train_file} // 챗봇학습용(답변용)데이터')
    print(f'user_dic_path = {user_dic_path} // 사용자정의사전')
    print(f'corpus_path = {corpus_path} // 의도분류모델(딥러닝모델)학습용데이터')
    print(f'chatbot_dict_path = {chatbot_dict_path} // 단어-정수 매핑데이터(pytorch의 lookuptable 또는 word2index)')
    print(f'intent_model_path = {intent_model_path} // 학습된 의도분류모델')
    print(f'intent_mapping_path = {intent_mapping_path} // 의도분류모델에서 사용된 레이블(y값) 정수매핑')
    print(f'ner_data_path1 = {ner_data_path1} //개체명 인식을 위한 유의어 원본 데이터')
    print(f'ner_data_path2 = {ner_data_path2} //개체명 인식을 위한 유의어 원본 데이터')
    print(f'ner_data_path3 = {ner_data_path3} //개체명 인식을 위한 유의어 원본 데이터')
    print(f'ner_data_path4 = {ner_data_path4} //개체명 인식을 위한 유의어 원본 데이터')
    print(f'ner_data_path5 = {ner_data_path5} //개체명 인식을 위한 유의어 원본 데이터')

    print(f'ner_final = {ner_final} //개체명 인식을 위한 데이터')
    print(f'timepoint_model_path = {timepoint_model_path} //날짜,시간인식을 위한 모델')
    print(f'jbotlog_directory_path = {jbotlog_directory_path} //클라이언트로부터 받은 jbot의 로그들이 저장될 폴더이름')