from central.dto import *

class RequestModel(BaseModel) :
    data : Optional[list]
    keyword : str
    brand_id: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    
class RecommendResult(BaseModel) :
    oid: str
    prob: float
    
class ResponseModel(BaseModel) :
    keyword: str
    folderUid: int
    refreshCount: int
    result: List[RecommendResult]

class ResponseMessage(BaseModel) :
    message: str