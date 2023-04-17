import sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
import pymysql
from jbot.config.DatabaseConfig import *

db = None

#챗봇 답변(학습)데이터 테이블 만들기!
db = None
try :
    #데이터베이스와 pymysql의 Connection객체 만들기
    #객체와 연결된 Connection객체 생성!
    db = pymysql.connect(
        host = DB_HOST,
        user = DB_USER,
        passwd = DB_PASSWORD,
        db =  DB_NAME,
    )
 
    #테이블 생성 sql 정의
    """
    테이블 이름 변경 chatbot_train_data => jbot_train_data
    컬럼추가 timepoint(시점),
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS `jbot_train_data` (
            `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            `intent` VARCHAR(45) NULL,
            `ner` VARCHAR(1024) NULL,
            `timepoint` VARCHAR(1024) NULL,
            `day` VARCHAR(1024) NULL,
            `detailloc` VARCHAR(1024) NULL,
            `answer` TEXT NOT NULL,
            `answer_image` VARCHAR(2048) NULL,
            PRIMARY KEY (`id`))
        ENGINE = InnoDB DEFAULT CHARSET=utf8
    '''

    #테이블 생성
    #db와 연결된 Connection객체의 cursor메서드로 pymysql의 Cursor객체를 만들어줌
    #db안에 있는 테이블을 sql구문으로 제어가능!
    with db.cursor() as curs:
        curs.execute(sql)
        print("생성")
except Exception as e:
    print(e)
    print("오류 ...")

finally:
    if db is not None:
        db.close()
        print("종료")