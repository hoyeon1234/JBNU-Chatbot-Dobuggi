import socket
class BotServer:
    def __init__(self,srv_port,listen_num):
        self.port = srv_port #서버의 포트번호
        self.listen = listen_num #허용할 스레드(동시요칭)의 갯수
        self.mySock = None
    
    def create_sock(self):
        self.mySock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.mySock.bind(("0.0.0.0",int(self.port))) #지정한 포트번호로
        self.mySock.listen(int(self.listen)) #지정한 연결 수 만큼의 클라이언트 연결을 수락하도록 합니다.
        return self.mySock
    def ready_for_client(self):
        return self.mySock.accept()
    def get_sock(self):
        return self.mySock