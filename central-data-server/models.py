import datetime

from tortoise import Model, fields

from central.enums import ProductType, Status
from fastapi_admin.models import AbstractAdmin

class Admin(AbstractAdmin):
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    email = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="https://s3.ap-northeast-2.amazonaws.com/prod.niz.ai/android-icon-36x36.png")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"

class Config(Model):
    label = fields.CharField(max_length=200)
    key = fields.CharField(max_length=20, unique=True, description="Unique key for config")
    value = fields.JSONField()
    status: Status = fields.IntEnumField(Status, default=Status.on)

class ClickhouseStopwords(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)

class WordDictAdjective(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_flag = fields.BooleanField(default=False)
    writer = fields.CharField(max_length=200)

class WordDictNoun(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_flag = fields.BooleanField(default=False)
    writer = fields.CharField(max_length=200)

class WordDictSuffix(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_flag = fields.BooleanField(default=False)
    writer = fields.CharField(max_length=200)

class WordDictTypo(Model):
    source_typo = fields.CharField(max_length=200, unique=True)
    target_typo = fields.CharField(max_length=200)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_flag = fields.BooleanField(default=False)
    writer = fields.CharField(max_length=200)
    
class TokenizerKiwiStopwords(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)

class TokenizerKiwiAdjectiveStopwords(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)

class TokenizerStopwords(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)
    
class TokenizerBackAdjective(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)
    
class TokenizerBackwords(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)
    
class TokenizerUnitwords(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)
    
class TokenizerPreBuildUnit(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)
    
class TokenizerKoNum(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)

class TokenizerNotKoNum(Model):
    word = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    writer = fields.CharField(max_length=200)
    
class CategoryClassifier(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    type = fields.CharField(max_length=200)
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
class SentimentClassifier(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    type = fields.CharField(max_length=200)
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

class SpamClassifier(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    type = fields.CharField(max_length=200)
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

class DocTypeClassifier(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    type = fields.CharField(max_length=200)
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

class SubjectClassifier(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    type = fields.CharField(max_length=200)
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
class TextToTensor(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
class PowerScore(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
class DocumentRecommender(Model) :
    name = fields.CharField(max_length=200)
    address = fields.TextField()
    external_address = fields.TextField()
    sort = fields.IntField()
    version = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)