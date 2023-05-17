from central.api import *

router = APIRouter()

@router.post("/analyze",response_model=dto.analyzer.power_score.ResponseModel)
async def power_score(data: dto.analyzer.power_score.RequestModel):
    model_info = await control.get_info("PowerScore")
    address = [obj.get('address') for obj in model_info][0]
    result = await control.requests_http(
        address=address,
        data=data.__dict__
    )
    response = dto.analyzer.power_score.ResponseModel(
        period=result.get("period"),
        score=result.get("score")
    )
    return response