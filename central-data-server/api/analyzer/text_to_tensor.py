from central.api import *

router = APIRouter()

@router.post("/analyze",response_model=dto.analyzer.text_to_tensor.ResponseModel)
async def text_to_tensor(data: dto.analyzer.text_to_tensor.RequestModel):
    model_info = await control.get_info("TextToTensor")
    address = [obj.get('address') for obj in model_info][0]
    result = await control.requests_http(
        address=address,
        data=data.__dict__
    )
    response = dto.analyzer.text_to_tensor.ResponseModel(
        input_ids=result.get("input_ids"),
        attention_mask=result.get("attention_mask")
    )
    return response