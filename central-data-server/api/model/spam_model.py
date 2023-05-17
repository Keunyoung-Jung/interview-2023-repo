from central.api import *

router = APIRouter()

@router.get("/info",response_model= List[dto.InfoResponse])
async def spam_model_info() :
    model_info = await control.get_info("SpamClassifier")
    response = [
        dto.InfoResponse(
            name = info.get('name'),
            address = info.get('address'),
            external_address=info.get('external_address'),
            sort = info.get('sort'),
            version = info.get('version'),
            created_at = info.get('created_at')
        ) for info in model_info
    ]
    return response

@router.post("/classify",response_model=dto.model.spam_model.ResponseModel)
async def spam_classifier(data: dto.model.spam_model.RequestModel):
    response = await control.spam_model.classify(
        text=data.text,
        version=data.version
        )
    return response