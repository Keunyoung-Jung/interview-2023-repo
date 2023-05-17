from pydantic import BaseModel
from typing import Optional, List, Union, Any
from datetime import datetime

class BaseTextRequest(BaseModel) :
    text: str
    channel: Optional[str]
    version: Optional[int] = 1
    
class UpdateWord(BaseModel) :
    word: Union[str,List[str]]
    
class UpdateTypo(BaseModel) :
    source_typo: str
    target_typo: str
    
class BaseResponse(BaseModel) :
    model: str
    result: str
    
class InfoResponse(BaseModel) :
    name : str
    address : str
    external_address: str
    sort : int
    version : int
    created_at : Union[datetime]

from central.dto.model import *
from central.dto.analyzer import *