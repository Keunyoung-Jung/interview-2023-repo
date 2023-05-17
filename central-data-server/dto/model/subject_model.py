from central.dto import *

class RequestModel(BaseTextRequest) :
    pass
    
class SubjectResult(BaseModel) :
    subject: str
    result: bool
    classIndex: int
    prob: float

class ResponseModel(BaseResponse) :
    result: List[SubjectResult]