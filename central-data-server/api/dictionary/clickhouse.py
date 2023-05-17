from central.api import *

router = APIRouter()

@router.get("/stopwords",response_model=List[str])
async def clickhouse_stopwords():
    response = await control.get_words("ClickhouseStopwords")
    return response