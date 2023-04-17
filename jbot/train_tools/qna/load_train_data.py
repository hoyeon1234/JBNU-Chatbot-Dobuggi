import sys
import pymysql
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
import openpyxl

"""
엑셀로 만들어진 챗봇 학습(답변)데이터를 MySQL DB와 동기화하는 코드입니다.
챗봇 학습(답변)데이터 관련 툴이기 때문에 train_tools/qna 디렉터리에 생성했습니다
"""


######################################

def all_clear_train_data(db): 
    """
    데이터베이스의 jbot_train_data테이블의 모든 관측치를 삭제하는 함수(초기화 함수)  
    Parameters

    db : Mysql 데이터베이스와 연결된 pymysql의 connection 객체
    """
    sql = '''
        delete from jbot_train_data
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)
    
    sql = '''
        ALTER TABLE jbot_train_data AUTO_INCREMENT = 1
    '''
    with db.cursor() as cursor:
        cursor.execute(sql)

def insert_data(db,xls_row): 
    """
    데이터베이스의 jbot_train_data테이블에 관측치(row)를 추가하는 함수
    Parameters
    db : pymysql의 connection 객체
    xls_row : openpyxl로 읽어들인 행
    수정해야한다면 
    1. xls_row 언패킹 변수 추가(또는 삭제)
    2. sql구문 문자열포매팅 2개다 수정(%s,변수)
    """
    _,intent,ner,timepoint,day,detailloc,answer,answer_image = xls_row
    if answer.value is not None:
        sql = '''
            INSERT jbot_train_data(intent,ner,timepoint,day,detailloc,answer,answer_image) 
            values(
                '%s','%s','%s','%s','%s','%s' ,'%s'
            )
        ''' % (intent.value,ner.value,timepoint.value,day.value,detailloc.value,answer.value,answer_image.value)
    else:
        sql = '''
            INSERT jbot_train_data(intent,ner,timepoint,day,detailloc,answer,answer_image) 
            values(
                '%s','%s','%s','%s','%s','%s','%s'
            )
        ''' % (intent.value,ner.value,timepoint.value,day.value,detailloc.value,"데이터가 없습니다.",answer_image.value)
    #상세설명 :
    #sql구문은 다음과 같이 입력해야 함 Insert jobt_train_data(컬럼명1,컬렴명2) values ('추가할값1','추가할값2')
    #그러므로 문자열포맷팅을 해서 값을 입력받도록함.
    sql = sql.replace("'None'",'null') #sql은 null을 알아먹으로 None을 null로 치환,str객체의 replace메서드 사용
    with db.cursor() as cursor:
        cursor.execute(sql)
        db.commit()
        print('저장완료')

##########################################
#엑셀파일 읽어와서 DB와 데이터 동기화 하기
db = None
try:
    db = pymysql.connect(host = DB_HOST,user = DB_USER,password = DB_PASSWORD,database = DB_NAME,charset = 'utf8')
    #기존 학습 데이터 초기화
    all_clear_train_data(db)
    #학습데이터 하나씩 추가
    wb = openpyxl.load_workbook(train_file)
    sheet = wb["Sheet1"]
    for row in sheet.iter_rows(min_row = 2): #min_row = 2 => 헤더는 불러오지 않음
        print(row)
        insert_data(db,row)
    wb.close()
except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()