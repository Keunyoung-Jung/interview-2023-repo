from datetime import datetime
from central.api import *

router = APIRouter()

@router.get("/adjective",response_model=List[str])
async def word_dict_adjective(updated_flag:bool=None,created_at:date=None):
    if updated_flag != None:
        response = await control.get_not_updated_words("WordDictAdjective",updated_flag)
    elif created_at != None:
        response = await control.find_gte_created("WordDictAdjective",created_at)
    else :
        response = await control.get_words("WordDictAdjective")
    return response

@router.patch("/adjective",response_model=bool)
async def word_dict_update_adjective(data: dto.UpdateWord):
    response = await control.update_words("WordDictAdjective",data.word)
    return response

@router.get("/noun",response_model=List[str])
async def word_dict_noun(updated_flag:bool=None,created_at:date=None):
    if updated_flag != None:
        response = await control.get_not_updated_words("WordDictNoun",updated_flag)
    elif created_at != None:
        response = await control.find_gte_created("WordDictNoun",created_at)
    else :
        response = await control.get_words("WordDictNoun")
    return response

@router.patch("/noun",response_model=bool)
async def word_dict_update_noun(data: dto.UpdateWord):
    response = await control.update_words("WordDictNoun",data.word)
    return response

@router.get("/suffix",response_model=List[str])
async def word_dict_suffix(updated_flag:bool=None,created_at:date=None):
    if updated_flag != None:
        response = await control.get_not_updated_words("WordDictSuffix",updated_flag)
    elif created_at != None:
        response = await control.find_gte_created("WordDictSuffix",created_at)
    else :
        response = await control.get_words("WordDictSuffix")
    return response

@router.patch("/suffix",response_model=bool)
async def word_dict_update_suffix(data: dto.UpdateWord):
    response = await control.update_words("WordDictSuffix",data.word)
    return response

@router.get("/typo",response_model=List[List[str]])
async def word_dict_typo(updated_flag:bool=None,created_at:date=None):
    if updated_flag != None:
        response = await control.get_not_updated_typos("WordDictTypo",updated_flag)
    elif created_at != None:
        response = await control.find_gte_created_typo("WordDictTypo",created_at)
    else :
        response = await control.get_typos("WordDictTypo")
    return response

@router.patch("/typo",response_model=bool)
async def word_dict_update_typo(data: dto.UpdateTypo):
    response = await control.update_typo("WordDictTypo",data.source_typo,data.target_typo)
    return response