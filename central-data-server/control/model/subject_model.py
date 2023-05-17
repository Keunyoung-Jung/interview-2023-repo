from central import control
from central import dto

async def classify(text, channel, version = 1) :
    model_name="SubjectClassifier"
    model_object = await control.get_model_addr_pipeline(
        model_name=model_name,
        version=version
        )
    
    response = dto.model.subject_model.ResponseModel(
        model = model_name,
        result = []
    )
    
    model_results = await control.requests_http_multi(
        model_object=model_object,
        data={"text":text},
        channel=channel
    )

    for model_result in model_results:
        model = dto.model.subject_model.SubjectResult(
            subject = model_result.get('name'),
            result = True,
            classIndex= model_result['result'].get('result'),
            prob = model_result['result'].get('prob')
        )
        if model_result['result'].get('result') > 0 :
            model.result = True
        else :
            model.result = False
        response.result.append(model)
    
    return response