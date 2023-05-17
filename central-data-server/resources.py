import os
from typing import List, Optional

from starlette.requests import Request
from starlette.datastructures import FormData
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND

from tortoise import Model as TortoiseModel
from central import enums
from central.constants import BASE_DIR
from central.models import *
from fastapi_admin.app import app
from fastapi_admin.enums import Method
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import Action, Dropdown, Field, Link, Model, ToolbarAction
from fastapi_admin.widgets import displays, filters, inputs
from central import control

upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))


@app.register
class Dashboard(Link):
    label = "홈"
    icon = "fas fa-home"
    url = "/admin"

@app.register
class GuideDocument(Link):
    label= "가이드 문서"
    icon = "fas fa-book"
    url = "/admin/guide"

@app.register
class AdminResource(Model):
    label = "유저"
    model = Admin
    icon = "fas fa-user"
    page_pre_title = "유저"
    page_title = "유저 목록"
    filters = [
        filters.Search(
            name="username",
            label="유저명",
            search_mode="contains",
            placeholder="유저명으로 검색하세요",
        ),
        filters.Date(name="created_at", label="생성일"),
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]

    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        return []

    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        if field.name == "id":
            return {"class": "bg-danger text-white"}
        return await super().cell_attributes(request, obj, field)

    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []

@app.register
class ModelResource(Dropdown):
    class CategoryClassifierResource(Model):
        page_pre_title = "AI 모델"
        page_title = "카테고리 분류"
        label = "카테고리 분류"
        model = CategoryClassifier
        fields = ["id", "name","address","external_address","type","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]
        
    class SentimentClassifierResource(Model):
        page_pre_title = "AI 모델"
        page_title = "감정 분류"
        label = "감정 분류"
        model = SentimentClassifier
        fields = ["id", "name","address","external_address","type","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]
    
    class SpamClassifierResource(Model):
        page_pre_title = "AI 모델"
        page_title = "스팸 분류"
        label = "스팸 분류"
        model = SpamClassifier
        fields = ["id", "name","address","external_address","type","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]
        
    class DocTypeClassifierResource(Model):
        page_pre_title = "AI 모델"
        page_title = "문서 타입 분류"
        label = "문서 타입 분류"
        model = DocTypeClassifier
        fields = ["id", "name","address","external_address","type","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]
    
    class SubjectClassifierResource(Model):
        page_pre_title = "AI 모델"
        page_title = "문서 주제 분류"
        label = "문서 주제 분류"
        model = SubjectClassifier
        fields = ["id", "name","address","external_address","type","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]

    label = "AI 모델"
    icon = "fas fa-cubes"
    resources = [
        CategoryClassifierResource,
        SentimentClassifierResource,
        SpamClassifierResource,
        DocTypeClassifierResource,
        SubjectClassifierResource
    ]

@app.register
class AnalyzerResource(Dropdown):
    class TextToTensorResource(Model):
        page_pre_title = "데이터 분석"
        page_title = "TextToTensor 전처리"
        label = "TextToTensor 전처리"
        model = TextToTensor
        fields = ["id", "name","address","external_address","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]
    
    class PowerScoreResource(Model):
        page_pre_title = "데이터 분석"
        page_title = "영향력 점수"
        label = "영향력 점수"
        model = PowerScore
        fields = ["id", "name","address","external_address","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]
        
    class DocumentRecommenderResource(Model):
        page_pre_title = "데이터 분석"
        page_title = "NIZ 문서 추천"
        label = "NIZ 문서 추천"
        model = DocumentRecommender
        fields = ["id", "name","address","external_address","sort","version", "created_at"]
        filters = [
            filters.Date(name="created_at", label="생성일"),
        ]

    label = "데이터 분석"
    icon = "fas fa-database"
    resources = [
        TextToTensorResource,
        PowerScoreResource,
        DocumentRecommenderResource
    ]

@app.register
class NizKeywordResource(Dropdown):
    class ClickhouseStopwordsResource(Model):
        page_pre_title = "NIZ 키워드"
        page_title = "불용어"
        label = "불용어"
        model = ClickhouseStopwords
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("ClickhouseStopwords") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret

    label = "NIZ 키워드"
    icon = "fas fa-hashtag"
    resources = [ClickhouseStopwordsResource]

@app.register
class WordDictResource(Dropdown):
    class WordDictAdjectiveResource(Model):
        page_pre_title = "단어 사전"
        page_title = "형용사"
        label = "형용사"
        model = WordDictAdjective
        fields = ["id", "word","writer", "created_at","updated_flag"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("WordDictAdjective") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class WordDictNounResource(Model):
        page_pre_title = "단어 사전"
        page_title = "명사"
        label = "명사"
        model = WordDictNoun
        fields = ["id", "word","writer", "created_at","updated_flag"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("WordDictNoun") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class WordDictSuffixResource(Model):
        page_pre_title = "단어 사전"
        page_title = "접미사"
        label = "접미사"
        model = WordDictSuffix
        fields = ["id", "word","writer", "created_at","updated_flag"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("WordDictSuffix") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class WordDictTypoResource(Model):
        page_pre_title = "단어 사전"
        page_title = "맞춤법 수정"
        label = "맞춤법 수정"
        model = WordDictTypo
        fields = ["id", "source_typo", "target_typo","writer", "created_at","updated_flag"]
        filters = [
            filters.Search(
                name="source_typo",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
    
    label = "단어 사전"
    icon = "fas fa-book"
    resources = [
        WordDictNounResource,
        WordDictAdjectiveResource,
        WordDictSuffixResource,
        WordDictTypoResource
    ]

@app.register
class TokenizerResource(Dropdown):
    class TokenizerKiwiStopwordsResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "[Kiwi]명사 불용어"
        label = "[Kiwi]명사 불용어"
        model = TokenizerKiwiStopwords
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerKiwiStopwords") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class TokenizerKiwiAdjectiveStopwordsResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "[Kiwi]형용사 불용어"
        label = "[Kiwi]형용사 불용어"
        model = TokenizerKiwiAdjectiveStopwords
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerKiwiAdjectiveStopwords") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class TokenizerStopwordsResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "[OKT]불용어"
        label = "[OKT]불용어"
        model = TokenizerStopwords
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerStopwords") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class TokenizerBackAdjectiveResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "의존 형용사 (앞 단어에 의존적일때 더 큰 의미를 가지는 형용사)"
        label = "의존 형용사"
        model = TokenizerBackAdjective
        fields = ["id", "word", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerBackAdjective") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class TokenizerBackwordsResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "의존 명사 (앞 단어에 의존적일때 더 큰 의미를 가지는 명사)"
        label = "의존 명사"
        model = TokenizerBackwords
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerBackwords") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class TokenizerUnitwordsResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "단위 명사 (SNS 혹은 일반적인 단위로 사용되는 명사)"
        label = "단위 명사"
        model = TokenizerUnitwords
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerUnitwords") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
        
    class TokenizerKoNumResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "한글 숫자 (한글로 표현된 숫자)"
        label = "한글 숫자"
        model = TokenizerKoNum
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerKoNum") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret
    
    class TokenizerNotKoNumResource(Model):
        page_pre_title = "토크나이저 후처리 사전"
        page_title = "한글 숫자 예외 (한글로 표현된 숫자중 예외처리 목록)"
        label = "한글 숫자 예외"
        model = TokenizerNotKoNum
        fields = ["id", "word","writer", "created_at"]
        filters = [
            filters.Search(
                name="word",
                label="단어",
                search_mode="contains",
                placeholder="단어를 검색하세요.",
            ),
            filters.Date(name="created_at", label="생성일"),
        ]
        async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
            ret = []
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                name = input_.context.get("name")
                if field.name == 'writer' :
                    ret.append(await input_.render(request, getattr(obj, name, str(request.state.admin).split('#')[1])))
                    continue
                if isinstance(input_, inputs.DisplayOnly):
                    continue
                ret.append(await input_.render(request, getattr(obj, name, None)))
            return ret
        
        async def resolve_data(cls, request: Request, data: FormData):
            ret = {}
            m2m_ret = {}
            for field in cls.get_fields(is_display=False):
                input_ = field.input
                if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                    continue
                name = input_.context.get("name")
                if isinstance(input_, inputs.ManyToMany):
                    v = data.getlist(name)
                    value = await input_.parse_value(request, v)
                    m2m_ret[name] = await input_.model.filter(pk__in=value)
                else:
                    v = data.get(name)
                    value = await input_.parse_value(request, v)
                    if value is None:
                        continue
                    if field.name == 'word' and value in await control.get_words("TokenizerNotKoNum") :
                        raise ValueError("Duplicate Error")
                    ret[name] = value
            return ret, m2m_ret

    label = "토크나이저 후처리 사전"
    icon = "fas fa-magic"
    resources = [
        TokenizerKiwiStopwordsResource,
        TokenizerKiwiAdjectiveStopwordsResource,
        TokenizerStopwordsResource,
        TokenizerBackAdjectiveResource,
        TokenizerBackwordsResource,
        TokenizerUnitwordsResource,
        TokenizerKoNumResource,
        TokenizerNotKoNumResource
    ]

@app.register
class ConfigResource(Model):
    label = "Config"
    model = Config
    icon = "fas fa-cogs"
    filters = [
        filters.Enum(enum=enums.Status, name="status", label="Status"),
        filters.Search(name="key", label="Key", search_mode="equal"),
    ]
    fields = [
        "id",
        "label",
        "key",
        "value",
        Field(
            name="status",
            label="Status",
            input_=inputs.RadioEnum(enums.Status, default=enums.Status.on),
        ),
    ]

    async def row_attributes(self, request: Request, obj: dict) -> dict:
        if obj.get("status") == enums.Status.on:
            return {"class": "bg-green text-white"}
        return await super().row_attributes(request, obj)

    async def get_actions(self, request: Request) -> List[Action]:
        actions = await super().get_actions(request)
        switch_status = Action(
            label="Switch Status",
            icon="ti ti-toggle-left",
            name="switch_status",
            method=Method.PUT,
        )
        actions.append(switch_status)
        return actions
