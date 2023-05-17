from central.dto import *
from enum import Enum

class ChannelEnum(Enum) :
    twitter = 'twitter'
    naver_blog = 'naver-blog'
    naver_cafe = 'naver-cafe'
    naver_news = 'naver-news'
    instagram = 'instagram'
    todayhumor = 'todayhumor'
    bobaedream = 'bobaedream'
    humoruniv = 'humoruniv'
    youtube = 'youtube'
    ppomppu = 'ppomppu'
    dcinsied = 'dcinside-gall'
    
class IncludeEnum(Enum) :
    target_keyword = "targetKeyword"
    uploaded_at = "uploadedAt"
    crawled_at = "crawledAt"
    channel = "channel"
    title = "title"
    engagement = "engagement"
    power_score = "powerScore"
    sentiment = "sentiment"
    category = "category"
    doc_type = "docType"
    spam_category = "spamCategory"

class RequestModel(BaseModel) :
    size_per_channel : int = 10
    target_keyword: Optional[List[str]] = ["키워드이름"]
    start_date : Optional[datetime] = None
    end_date : Optional[datetime] = None
    channel : Optional[List[ChannelEnum]] = list(ChannelEnum._member_map_.values())
    search_keyword: Optional[List[str]] = None
    include : Optional[List[IncludeEnum]] = []

class ResponseModel(BaseModel) :
    documents : List[Any]
