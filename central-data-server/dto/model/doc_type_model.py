from central.dto import *

class RequestModel(BaseTextRequest) :
    pass
    
class DocTypeResult(BaseModel) :
    docType: str
    result: bool
    classIndex: int
    prob: float

class ResponseModel(BaseResponse) :
    result: List[DocTypeResult]