# Example DataLoader project
s3에 업로드된 Parquet 파일을 훈련에 사용하기 위한 DataLoader를 사용합니다.    
    
[s3_loader.py](s3_loader.py)를 이용해서 parquet파일을 불러올 수 있습니다.   
DataLoader는 pandas dataframe을 반환합니다.   
## Dependency
* **parquet-loader**
* ~~s3fs~~
* ~~fastparquet~~
* ~~pandas==1.2.0~~
## How to use
### S3 Setting
DataLoader는 S3프로토콜을 기반으로 동작합니다.   
S3 환경 변수가 올바르게 설정되어 있어야 합니다.   
```bash
export AWS_ACCESS_KEY_ID=my-access-key
export AWS_SECRET_ACCESS_KEY=my-secret-key
export AWS_DEFAULT_REGION=ap-northeast-2
```
```shell
pip3 install parquet-loader
```
### Initialize
DataLoader 클래스를 선언합니다.
```python
from ParquetLoader import S3Loader

data_loader = S3Loader(
        bucket='mysterico-feature-store',
        folder="mongo-sentence-token-feature",
        depth=2)

for df in data_loader :
    print(df.head())
```
### property check
데이터를 로드하기 전에 속성을 확인하고 columns을 지정할 수 있습니다.
```python
print(data_loader.count)
print(data_loader.columns)
# 로드할 데이터의 columns을 지정
data_loader.select_columns = ['brandId','Tokens']
```
output
```
975633
['objectId', 'brandId', 'Tokens', 'createdAt', 'createdYear', 'createdMonth', 'createdDay']
```
### using loader
DataLoader 클래스는 Generator로 생성되어 동작됩니다.   
따라서, Generator에서 사용하는 next함수나, for loop를 통한 iteration을 사용합니다.
```python
first_df = next(data_loader)
second_df = next(data_loader)

for df in data_loader:
    df_cache = df
```
## Data Location
현재 연구용 데이터는 S3 Storage에 매일 업데이트 됩니다.   
Bucket은 `mysterico-feature-store`를 이용합니다. (default로 설정되어 있습니다.)   
데이터를 불러오기 위해 Initialize하는 시간이 **1~2분** 소요됩니다.
   
**가져올 수 있는 데이터 목록**   
|folder|설명|Schema|initialize time|
|--|--|--|--|
|`mongo-raw-feature.parquet`|몽고DB 데이터를 테이블 형태로 반환|[raw-feature 스키마](schema/raw-feature-schema.md)|110.42sec|
|`mongo-document-token-feature.parquet`|문서 그대로 Tokenizing된 결과|[document-token-feature 스키마](schema/document-token-schema.md)|88.24sec|
|`mongo-sentence-feature.parquet`|문서를 문장으로 분리한 결과|[sentence-feature 스키마](schema/sentence-feature.md)|80.55sec|
|`mongo-sentence-token-feature.parquet`|문서를 문장으로 분리한뒤 해당 문장을 Tokenizing한 결과|[sentence-token-feature 스키마](schema/sentence-token-schema.md)|54.69sec|