### mongo-sentence-token-feature.parquet 스키마
|Column|information|datatype|
|--|--|--|
|`objectId`|ObjectId|*string*| 
|`brandId`|브랜드 명|*string*| 
|`channelKeyname`|채널 이름|*string*|
|`sentence`|<span style="color:orange">분리된 문장의 한 문장</span>|*string*| 
|`tokens`|<span style="color:orange">한 문장의 Word Token</span>|*array[string]*| 
|`hashTag`|<span style="color:orange">해시태그 리스트</span>|*array[string]*| 
|`sentimentAnalysisResult`|감성 분류 결과|*integer*| 
|`isDeleted`|삭제 여부|*boolean*| 
|`uploadedAt`|업로드 일자|*timestamp*| 
|`uploadedYear`|업로드 연도|*integer*|
|`uploadedMonth`|업로드 월|*integer*|
|`uploadedDay`|업로드 일|*integer*| 
|`uploadedDayName`|업로드 요일명|*string*| 
|`uploadedWeek`|업로드된 n주차|*integer*| 