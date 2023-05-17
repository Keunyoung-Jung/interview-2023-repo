from central.dto import *

class RequestModel(BaseModel) :
    channel: str
    targetDate: str
    commentCount: int
    likeCount: int
    dislikeCount: int
    shareCount: int
    viewCount: int
    
class ResponseModel(BaseModel) :
    period: str
    score: float