from central import control
from central import dto

async def classify(text, version = 1) :
    model_name="CategoryClassifier"
    model_address = await control.get_model_addr(
        model_name=model_name,
        version=version
    )
    model_result = await control.requests_http(
        address=model_address,
        data={"text":text}
    )
    category_result = []
    for key, value in model_result.items() :
        model = dto.model.category_model.CategoryResult(
            category = key,
            rank = value,
            result = True
        )
        if 0 < value < 255:
            model.result = True
        else :
            model.result = False
        category_result.append(model)
    
    response = dto.model.category_model.ResponseModel(
        model = model_name,
        result = category_result
    )
    
    return response