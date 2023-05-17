### mongo-raw-feature.parquet 스키마
|Column|information|datatype|
|--|--|--|
|`_id.oid`|mongoDB oid|*string*|
|`articleCode`|아티클 코드|*string*|
|`articleType`|아티클 타입|*string*|
|`brandId`|브랜드명|*string*|
|`cafeKeyname`|카페 키 이름|*string*|
|`channelKeyname`|채널 이름|*string*|
|`crc`|crc|*sring*|
|`createdAt`|생성 일자|*timestamp*|
|`deletedAt`|삭제 일자|*timestamp*|
|`deletedId`|삭제된 Id|*string*|
|`deleterId`|삭제한 유저Id|*string*|
|`isDeleted`|삭제 여부 표시|*boolean*|
|`sentimentAnalysisProb`|감성 모델 점수|*double*|
|`sentimentAnalysisResult`|감성 분류 결과|*integer*|
|`trainedAt`|감성 수정 일자|*timstamp*|
|`trainedResult`|감성 수정 결과|*integer*|
|`trainerId`|감성 수정 Id|*string*|
|`updatedAt`|업데이트 일자|*timstamp*|
|`detailData._id.oid`|문서의 mongo oid|*string*|
|`detailData.pageUrl`|문서의 url|*string*|
|`detailData.apiUrl`|문서의 api url|*string*|
|`detailData.postImage`|문서의 이미지|*string*|
|`detailData.postTitle`|문서의 제목|*string*|
|`detailData.profilePhoto`|문서의 프로필 이미지|*string*|
|`detailData.content`|문서의 본문|*string*|
|`detailData.contentPlainText`|문서의 clean 텍스트|*string*|
|`detailData.isTransaction`|문서의 ??|*boolean*|
|`detailData.location`|문서에 나타난 주소|*string*|
|`detailData.callCount`|문서의 call 수(?)|*integer*|
|`detailData.favoriteCount`|문서의 북마크 수(?)|*integer*|
|`detailData.commentCount`|문서의 댓글 수|*double*|
|`detailData.likeCount`|문서의 좋아요 수|*integer*|
|`detailData.dislikeCount`|문서의 싫어요 수|*integer*|
|`detailData.shareCount`|문서의 공유 수|*integer*|
|`detailData.viewCount`|문서의 조회 수|*integer*|
|`detailData.thumbnails`|문서의 썸네일 리스트|*array[string]*|
|`detailData.uploadedAt`|문서가 업로드된 일자|*timestamp*|
|`detailData.uploaderId`|문서를 업로드한 userId|*string*|
|`detailData.uploaderName`|문서를 업로드한 user명|*string*|
|`uploadedYear`|문서를 업로드한 연도|*integer*|
|`uploadedMonth`|문서를 업로드한 월|*integer*|
|`uploadedDay`|문서를 업로드한 일자|*integer*|