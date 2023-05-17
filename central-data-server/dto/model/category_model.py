from central.dto import *

class RequestModel(BaseTextRequest) :
    pass
    
class CategoryResult(BaseModel) :
    category: str
    result: bool
    rank: int
    
class ResponseModel(BaseResponse) :
    result: List[CategoryResult]