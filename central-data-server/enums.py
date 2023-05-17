from enum import Enum, IntEnum


class ProductType(IntEnum):
    article = 1
    page = 2


class Status(IntEnum):
    on = 1
    off = 0


class Action(str, Enum):
    create = "생성"
    delete = "삭제"
    edit = "수정"
