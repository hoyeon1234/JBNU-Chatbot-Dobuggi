#챗봇학습데이터 데이터베이스 접속 정보

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "0000"
DB_NAME = "homestead"

def DatabaseConfig():
    global DB_HOST,DB_USER,DB_PASSWORD,DB_NAME
    print(f'DB_HOST = {"127.0.0.1"}, DB_USER = {DB_USER}, DB_PASSWORD = {DB_PASSWORD}, DB_NAME = {DB_NAME}')
