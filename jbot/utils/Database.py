import sys
pckg_path = "C:/Users/22668/Desktop"
sys.path.append(pckg_path)
from jbot.config.DatabaseConfig import *
from jbot.config.PathConfig import *
import pymysql
import pymysql.cursors
import logging

class Database:
    """
    Database 객체,db와 연결 and 제어
    """
    def __init__(self,host,user,password,db_name,charset = "utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.db_name = db_name
        self.conn = None
    def connect(self):
        """
        pymysql의 Connection객체를 생성하여 db와 연결합니다.
        """
        if self.conn != None: 
            #이미 연결이 되어있는경우 다시 연결하지 않음
            return
        self.conn = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            db = self.db_name,
            charset = self.charset
        )
        print("db와 연결시작")
    def close(self):
        if self.conn is None:
            #연결이 없는 경우 그냥 종료
            return 
        if not self.conn.open == None:
            #커넥션이 오픈되어있지 않은 경우도 그냥 종료
            return
        self.conn.close() #먼저 연결을 닫고
        self.conn = None #커넥션객체도 제거
        print("db와 연결 종료")
    def execute(self,sql):
        """
        sql구문 실행하는 함수
        """
        last_row_id = -1
        try :
            with self.conn.cursor() as cursor: #sql문을 실행할 수 있게 해주는 pymysql의 cursor객체를 만든다
                cursor.execute(sql) #실행
            self.conn.commit() #커밋하여 db에 수정사항 반영
            last_row_id = cursor.lastrowid
        except Exception as ex:
            logging.error(ex)
        finally:
            return last_row_id
    def select_one(self,sql):
        """
        sql구문은 반드시 select구문이어야 함 !
        select구문을 입력하면 한개의 row(관측치)만 가져와주는 함수
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
        except Exception as ex:
            logging.error(ex)
        finally : 
            return result
    def select_all(self,sql):
        """
        sql구문은 반드시 select구문이어야 함 !
        select구문을 입력하면 전체 row(관측치)를 가져와주는 함수
        """
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        except Exception as ex:
            logging.error(ex)
        finally:
            return result
        
        


"""
db = Database(host = DB_HOST,user = DB_USER,db_name = DB_NAME,password = DB_PASSWORD)
db.connect()

sql = "select * from jbot_train_data"

obs = db.select_one(sql)
print(obs)
all_obs = db.select_all(sql)
print(all_obs)

db.close()
"""