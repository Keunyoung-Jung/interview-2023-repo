from tortoise import Tortoise
from fastapi.params import Path
from typing import List, Optional, Type
import aiohttp
from central import dto
import asyncio

def get_model(resource: Optional[str] = Path(...)):
    if not resource:
        return
    for app, models in Tortoise.apps.items():
        models = {key.lower(): val for key, val in models.items()}
        model = models.get(resource)
        if model:
            return model

async def get_words(model_name) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.values()
    words = [obj.get('word') for obj in query_values]
    return words

async def get_not_updated_words(model_name,updated_flag) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.filter(updated_flag=updated_flag).values()
    words = [obj.get('word') for obj in query_values]
    return words

async def find_gte_created(model_name,created_at):
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.filter(created_at__gte=created_at).values()
    words = [obj.get('word') for obj in query_values]
    return words

async def update_words(model_name,word) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    if type(word) == list :
        await asyncio.gather(*[query_set.filter(word=w).update(updated_flag=True) for w in word])
    else :
        await query_set.filter(word=word).update(updated_flag=True)
    return True

async def get_typos(model_name) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.values()
    words = [
        [obj.get('source_typo'),obj.get('target_typo')]
        for obj in query_values
    ]
    return words

async def find_gte_created_typo(model_name,created_at):
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.filter(created_at__gte=created_at).values()
    words = [
        [obj.get('source_typo'),obj.get('target_typo')]
        for obj in query_values
    ]
    return words

async def get_not_updated_typos(model_name,updated_flag) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.filter(updated_flag=updated_flag).values()
    words = [
        [obj.get('source_typo'),obj.get('target_typo')]
        for obj in query_values
    ]
    return words

async def update_typo(model_name,source_typo,target_typo) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    await query_set.filter(source_typo=source_typo,target_typo=target_typo).update(updated_flag=True)
    return True

async def get_info(model_name) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.values()
    return query_values

async def get_model_addr(model_name,version=1) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.filter(version=version).values()
    model_address = [obj.get('address') for obj in query_values][0]
    return model_address

async def get_model_addr_pipeline(model_name,version=1) :
    model_name = model_name.lower()
    model = get_model(model_name)
    query_set = model.all()
    query_values = await query_set.filter(version=version).values()
    model_address = [
        {
            "name" : obj.get('name'),
            "address" : obj.get('address'),
            "text_limit": obj.get('sort')
        } for obj in query_values
    ]
    return model_address
    
async def requests_http(address, data, method="POST",auth : aiohttp.BasicAuth = None) :
    if method == "POST" :
        async with aiohttp.ClientSession() as session:
            response = await _requests_http(session,address, data, auth)
        return response
    elif method == "GET":
        async with aiohttp.ClientSession() as session:
            response = await _requests_http_get(session,address, data, auth)
        return response

async def _requests_http_get(session,address, params, auth : aiohttp.BasicAuth = None) :
    if "http://" not in address :
        address = "http://"+address
        
    async with session.get(
        address,
        params=params,
        auth=auth
    ) as response :
        assert response.status < 400
        try :
            return await response.json()
        except :
            return response

async def _requests_http(session,address, data, auth : aiohttp.BasicAuth = None) :
    if "http://" not in address :
        address = "http://"+address
        
    async with session.post(
        address,
        json=data,
        auth=auth
    ) as response :
        assert response.status < 400
        try :
            return await response.json()
        except :
            return response
    
async def requests_http_multi(model_object, data, text_length=1, channel=None) :
    futures = []
    for mobj in model_object :
        if text_length < mobj.get('text_limit') :
            futures.append(
                asyncio.ensure_future(
                    requests_http(mobj.get('address'),{})
                )
            )
        elif channel not in ['naver-cafe','daum-cafe'] and mobj.get('name') == "cafe-activity" :
            futures.append(
                asyncio.ensure_future(
                    requests_http(mobj.get('address'),{})
                )
            )
        else :
            futures.append(
                asyncio.ensure_future(
                    requests_http(mobj.get('address'),data)
                )
            )
    result = await asyncio.gather(*futures)
    model_result = []
    for index,res in enumerate(result):
        model_result.append(
            {
                "name": model_object[index].get('name'),
                "result" : res
            }
        )
    return model_result
    
from central.control.model import *