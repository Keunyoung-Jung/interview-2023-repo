from central.api import *
import os
from aiohttp import BasicAuth
import asyncio
import random
from datetime import datetime
import pytz

router = APIRouter()

async def datetime_to_iso_string(date: datetime) -> str :
    return date.replace(microsecond=0).astimezone(pytz.timezone('Asia/Seoul')).isoformat()

async def get_data(params,channel):
    def base_search_query(searchKeyword) :
        fields = [
            [
                "detailData.contentPlainText.ignore",
                "detailData.contentPlainText.simple",
                "detailData.title.ignore",
                "detailData.title.simple"
            ],
            [
                "detailData.contentPlainText.openkoreantext",
                "detailData.title.openkoreantext"
            ],
            [
                "detailData.contentPlainText.nori_token",
                "detailData.contentPlainText.nori_ngram",
                "detailData.title.nori_token",
                "detailData.title.nori_ngram"
            ]
        ]
        
        should = [
            {
                "multi_match": {
                    "query": searchKeyword,
                    "type": "phrase",
                    "fields": field
                }
            }
            for field in fields
        ]
        
        return should
    
    def created_multi_search_query(search_keywords):
        multi_search_query = []
        for keyword in search_keywords:
            multi_search_query += base_search_query(keyword)
            
        return multi_search_query
    
    def create_include_list(include) :
        include_list = ["detailData.contentPlainText"]
        mapper = {
            "targetKeyword": ["targetKeyword"],
            "uploadedAt" : ["detailData.uploadedAt"],
            "crawledAt" : ["crawledAt"],
            "channel" : ["channelKeyname"],
            "title" : ["detailData.title"],
            "engagement" : [
                "detailData.likeCount",
                "detailData.dislikeCount",
                "detailData.commentCount",
                "detailData.shareCount",
                "detailData.viewCount"
            ],
            "powerScore" : ["powerScore"],
            "sentiment" : ["sentimentAnalysisResult"],
            "category" : ["categoryAnalysisResult"],
            "docType" : ["docType"],
            "spamCategory" : ["spamCategory"]
        }
        for inc in include :
            include_list += mapper[inc.value]
        return include_list
    
    def preprocess_es(response,include_list) :
        hits_list = response.get("hits").get("hits")
        return_list = []
        for hits in hits_list :
            return_dict = {}
            for include in include_list :
                pure_name = include.replace("detailData.","")
                if "detailData." in include :
                    return_dict[pure_name] = hits.get("_source").get("detailData").get(pure_name)
                else :
                    return_dict[pure_name] = hits.get("_source").get(pure_name)
            return_list.append(return_dict)
        return return_list

    include_list = create_include_list(params.include)
    query = {
        "size": params.size_per_channel,
        "_source":{
            "include":include_list
        },
        "query":{
            "function_score":{
                "query": {
                    "bool":{
                        "must":[
                            {
                                "term":{
                                    "channelKeyname": channel
                                }
                            }
                        ],
                        "must_not":[
                            {
                                "term":{
                                    "detailData.contentPlainText": ""
                                }
                            }
                        ]
                    }
                },
                "functions":[
                    {
                        "random_score": {},
                    }
                ],
                "boost_mode": "replace",
                "score_mode": "multiply"
            }
        }
    }
    
    additional_filter = query["query"]["function_score"]["query"]
    
    if params.start_date != None and params.end_date != None :
        additional_filter["bool"]["must"].append(
            {
                "range" : {
                    "detailData.uploadedAt": {
                        "gte": await datetime_to_iso_string(params.start_date),
                        "lte": await datetime_to_iso_string(params.end_date)
                    }
                }
            }
        )
    if params.search_keyword != None :
        additional_filter["bool"]["should"] = created_multi_search_query(params.search_keyword)
        additional_filter["bool"]["minimum_should_match"] = 1

    if params.target_keyword not in [["키워드이름"],None] :
        additional_filter["bool"]["must"].append(
            {
                "terms":{
                    "targetKeyword": params.target_keyword
                }
            }
        )

    address = os.environ["ELASTICSEARCH_URL"]
    response = await control.requests_http(
        address=address,
        data=query,
        auth=BasicAuth(
            os.environ["ELASTICSEARCH_USER"],
            os.environ["ELASTICSEARCH_PASSWORD"]
        )
    )
    
    return preprocess_es(response,include_list)

async def get_random_data(params) :
    data = await asyncio.gather(
        *[get_data(params,channel.value) for channel in params.channel]
    )
    data = sum(data, [])
    random.shuffle(data)
    return data

@router.post("/generate",response_model=dto.analyzer.niz_sample_data.ResponseModel)
async def niz_sample_data(data: dto.analyzer.niz_sample_data.RequestModel):
    result = await get_random_data(data)
    
    response = dto.analyzer.niz_sample_data.ResponseModel(
        documents=result
    )
    return response