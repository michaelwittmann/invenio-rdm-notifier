from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, AnyHttpUrl


class Version(BaseModel):
    is_latest: bool
    index: int
    is_latest_draft: bool


class PersonOrOrg(BaseModel):
    name: str


class Creator(BaseModel):
    person_or_org: PersonOrOrg


class Metadata(BaseModel):
    description: Optional[str] = None
    publisher: str
    title: str
    creators: Optional[List[Creator]] = []


class Links(BaseModel):
    self: AnyHttpUrl
    self_html: AnyHttpUrl
    latest_html: AnyHttpUrl


class Record(BaseModel):
    id: str
    updated: datetime
    is_draft: bool
    created: datetime
    status: str
    versions: Version
    metadata: Metadata
    links: Links


