from datetime import datetime
from typing import Optional, List

import requests

from pydantic import BaseModel, AnyHttpUrl, TypeAdapter

from src.invenio_rdm_datamodel.api import InvenioRDMAPI


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
    publisher: str | None = None
    title: str
    creators: Optional[List[Creator]] = []


class Links(BaseModel):
    self: AnyHttpUrl
    self_html: AnyHttpUrl
    latest_html: AnyHttpUrl


class OwnedBy(BaseModel):
    user: int


class Access(BaseModel):
    owned_by: List[OwnedBy] | None = []


class Communities(BaseModel):
    default: str | None = None
    ids: List[str] | None = []


class Parent(BaseModel):
    id: str
    access: Access
    communities: Communities | None = None


class Record(BaseModel):
    id: str
    updated: datetime
    is_draft: bool
    created: datetime
    status: str
    versions: Version
    metadata: Metadata
    links: Links
    parent: Parent


class RecordAPI(InvenioRDMAPI):

    @property
    def _url(self):
        return super()._url + "/records"

    def get_newest_records(self, n=10) -> List[Record]:
        params = {"sort": "newest",
                  "size": n}
        res = requests.get(f"{self._url}",
                           headers=self._auth_header,
                           params=params,
                           verify=False).json()
        records = TypeAdapter(List[Record]).validate_python(res['hits']['hits'])
        return records

