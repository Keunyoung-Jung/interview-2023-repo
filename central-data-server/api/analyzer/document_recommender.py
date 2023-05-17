from central.api import *

router = APIRouter()

@router.put("/control/regist",response_model=dto.analyzer.document_recommender.ResponseMessage, status_code=201)
async def regist_document_recommend(
    dev: bool = False
):
    model_info = await control.get_info("DocumentRecommender")
    address = [
        obj.get('address') 
        for obj in model_info 
        if obj.get('name') == 'Maker'
    ][0]
    endpoint = '/make-faiss-engine'
    if dev :
        endpoint = '/make-faiss-engine-test'
    message = await control.requests_http(
        address=address+endpoint,
        data={},
        method="GET"
    )
    response = dto.analyzer.document_recommender.ResponseMessage(
        message=message
    )
    return response

@router.patch("/control/brand",response_model=dto.analyzer.document_recommender.ResponseMessage, status_code=201)
async def update_document_recommend_brand(
    brandUid: int,
    dev: bool = False
):
    model_info = await control.get_info("DocumentRecommender")
    address = [
        obj.get('address') 
        for obj in model_info 
        if obj.get('name') == 'Updater'
    ][0]
    endpoint = '/make-brand-bookmark-recommended-document'
    data = {
        "brand_uid" : brandUid,
        "is_dev" : dev,
    }
    message = await control.requests_http(
        address=address+endpoint,
        data=data
    )
    response = dto.analyzer.document_recommender.ResponseMessage(
        message=message
    )
    return response

@router.patch("/control/folder",response_model=dto.analyzer.document_recommender.ResponseMessage, status_code=201)
async def update_document_recommend_folder(
    keyword: str,
    brandUid: int,
    folderUid: int,
    dev: bool = False
):
    model_info = await control.get_info("DocumentRecommender")
    address = [
        obj.get('address') 
        for obj in model_info 
        if obj.get('name') == 'Updater'
    ][0]
    endpoint = '/update-target-bookmark-folder-recommended-document'
    data = {
        "keyword" : keyword,
        "brand_uid" : brandUid,
        "folder_uid" : folderUid,
        "is_dev" : dev
    }
    message = await control.requests_http(
        address=address+endpoint,
        data=data
    )
    response = dto.analyzer.document_recommender.ResponseMessage(
        message=message
    )
    return response

@router.get("/analyze",response_model=dto.analyzer.document_recommender.ResponseModel)
async def document_recommend(
    keyword: str,
    folderUid: int,
    refreshCount: int,
    dev: bool = False,
):
    model_info = await control.get_info("DocumentRecommender")
    address = [
        obj.get('address') 
        for obj in model_info 
        if obj.get('name') == 'Giver'
    ][0]
    endpoint = '/get-recommended-document'
    data = {
        "keyword" : keyword,
        "folder_uid" : folderUid,
        "refresh_count" : refreshCount,
        "is_dev" : dev
    }
    result = await control.requests_http(
        address=address+endpoint,
        data=data
    )
    response = dto.analyzer.document_recommender.ResponseModel(
        keyword= keyword,
        folderUid= folderUid,
        refreshCount= refreshCount,
        result=[
            dto.analyzer.document_recommender.RecommendResult(
                oid=res["oid"],
                prob=res["prob"]
            )
            for res in result
        ]
    )
    return response