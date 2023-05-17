from central.api import *
import boto3, os

router = APIRouter()

s3 = boto3.client("s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="ap-northeast-2"
    )

@router.get("/{path}")
async def download_api(path:str,file:str) :
    if path[-1] != '/' :
        path = path+'/'
    aws_key_name = f'tokenizer/{path}{file}'
    try:
        result = s3.get_object(Bucket=os.getenv("AWS_S3_BUCKET"), Key=aws_key_name)
        headers = {
            'Content-Disposition': f'''attachment; filename="{file}"; filename*=utf-8''{quote(file)}'''
        }
        response = StreamingResponse(content=result["Body"].iter_chunks(), headers=headers)
        return response

    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=e.message["response"]["Error"]["Code"],
                detail=e.message["response"]["Error"]["Message"],
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))
    return response