from central import control
from central import dto

async def classify(text, version = 1) :
    model_name="SpamClassifier"
    model_address = await control.get_model_addr(
        model_name=model_name,
        version=version
        )
    model_result = await control.requests_http(
        address=model_address,
        data={"text":text}
    )
    response = dto.model.spam_model.ResponseModel(
        model = model_name,
        result = "ham",
        classIndex= model_result[0],
        prob = model_result[1]
    )
    
    if model_result[0] == 0 :
        response.result = "ham"
    elif model_result[0] == 1 :
        response.result = "spam"
    else :
        response.result = "unclassified"
    
    return response