from central import control
from central import dto

async def classify(text, version = 1) :
    model_name="SentimentClassifier"
    model_address = await control.get_model_addr(
        model_name=model_name,
        version=version
        )
    model_result = await control.requests_http(
        address=model_address,
        data={"text":text}
    )
    response = dto.model.sentiment_model.ResponseModel(
        model = model_name,
        result = "positive",
        classIndex= model_result.get('result'),
        prob = dto.model.sentiment_model.SentimentProb(
            positive=model_result.get('prob')[0],
            neutral=model_result.get('prob')[1],
            negative=model_result.get('prob')[2]
        )
    )
    
    if model_result.get('result') == 0 :
        response.result = "positive"
    elif model_result.get('result') == 1 :
        response.result = "neutral"
    elif model_result.get('result') == 2 :
        response.result = "negative"
    else :
        response.result = "unclassified"
    
    return response