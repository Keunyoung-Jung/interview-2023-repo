from central.dto import *

class RequestModel(BaseTextRequest) :
    tokenizer: Optional[str] = 'monologg/koelectra-base-v3-discriminator'

class ResponseModel(BaseModel) :
    input_ids: List[int]
    attention_mask: List[int]