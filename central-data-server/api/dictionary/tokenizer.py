from central.api import *

router = APIRouter()

@router.get("/kiwiStopwords",response_model=List[str])
async def tokenizer_kiwi_stopwords():
    response = await control.get_words("TokenizerKiwiStopwords")
    return response

@router.get("/kiwiAdjectiveStopwords",response_model=List[str])
async def tokenizer_kiwi_adj_stopwords():
    response = await control.get_words("TokenizerKiwiAdjectiveStopwords")
    return response

@router.get("/stopwords",response_model=List[str])
async def tokenizer_stopwords():
    response = await control.get_words("TokenizerStopwords")
    return response

@router.get("/backadj",response_model=List[str])
async def tokenizer_backadj():
    response = await control.get_words("TokenizerBackAdjective")
    return response

@router.get("/backwords",response_model=List[str])
async def tokenizer_backwords():
    response = await control.get_words("TokenizerBackwords")
    return response

@router.get("/unitwords",response_model=List[str])
async def tokenizer_unitwords():
    response = await control.get_words("TokenizerUnitwords")
    return response

@router.get("/pre_build_unit",response_model=List[str])
async def tokenizer_pre_build_unit():
    response = await control.get_words("TokenizerPreBuildUnit")
    return response

@router.get("/ko_num",response_model=List[str])
async def tokenizer_ko_num():
    response = await control.get_words("TokenizerKoNum")
    return response

@router.get("/not_ko_num",response_model=List[str])
async def tokenizer_not_ko_num():
    response = await control.get_words("TokenizerNotKoNum")
    return response