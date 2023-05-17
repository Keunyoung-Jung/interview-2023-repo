from central.api import *

router = APIRouter()

@router.get("/info",response_model= List[dto.InfoResponse])
async def subject_model_info() :
    model_info = await control.get_info("SubjectClassifier")
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

@router.post("/classify",response_model=dto.model.subject_model.ResponseModel)
async def subject_classifier(data: dto.model.subject_model.RequestModel):
    response = await control.subject_model.classify(
        text=data.text,
        channel=data.channel,
        version=data.version
        )
    return response