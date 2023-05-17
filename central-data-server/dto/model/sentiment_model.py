from central.dto import *

class RequestModel(BaseTextRequest) :
    pass
    
class SentimentProb(BaseModel) :
    positive: float
    neutral: float
    negative: float
    
class ResponseModel(BaseResponse) :
    prob: SentimentProb
    classIndex: int