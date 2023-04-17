class KakaoTemplate():
    def __init__(self):
        self.version = "2.0"
    
    def simpleTextComponent(self,text):
        #output 필드에 simpleText필드 추가
        return {
            "simpleText" : {"text" : text}
        }

    def simpleImageComponent(self,imageUrl,altText):
        #output 필드에 simpleImage필드 추가
        return {
            "simpleImage" : {"imageUrl":imageUrl,"altText":altText}
        }

    def send_response(self,bot_resp):
        #print("send response 함수 진입")
        """
        responseBody = {
            "version" : self.version, #버전은 2.0으로 항상 고정
            "template" : {
                "outputs" : []
            }
        }
        """
        responseBody = {
            "version" : self.version,
            "template" : {
                "outputs":[]
            }
        }
        #챗봇서버가 이미지 url을 반환하면
        img_response = bot_resp["AnswerImageUrl"]
        if img_response is not None:
             responseBody["template"]["outputs"].append(self.simpleImageComponent(img_response))
        #print("1rebody",responseBody)
        text_response = bot_resp["Answer"]
        #챗봇서버가 텍스트를 반환하면
        if text_response is not None:
            responseBody["template"]["outputs"].append(self.simpleTextComponent(text_response)) 
        return responseBody