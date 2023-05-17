from central.dto import *

class RequestModel(BaseTextRequest) :
    pass
    
class ResponseModel(BaseResponse) :
    prob: float
    classIndex: int