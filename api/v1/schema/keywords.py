import typing
from pydantic import BaseModel


class News(BaseModel):
    id: str
    pubdate: str
    title: str
    text: str
    keywords: typing.List[str]
    producer: typing.Dict[
        str,
        typing.Union[
            int, str, typing.List[typing.Dict[str, typing.Union[str, float]]]
        ],
    ]
    volume_now: float
    volume_yesterday: float


class KeywordList(BaseModel):
    keyword: typing.List[str]
    News: typing.List[News]
