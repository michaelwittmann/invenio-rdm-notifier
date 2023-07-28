import requests
from pydantic import BaseModel, AnyHttpUrl, TypeAdapter

from src.invenio_rdm_datamodel.api import InvenioRDMAPI


class Metadata(BaseModel):
    title: str
    website: AnyHttpUrl | None = None


class Community(BaseModel):
    revision_id: int
    metadata: Metadata
    id: str
    slug: str


class CommunityAPI(InvenioRDMAPI):
    @property
    def __url(self):
        return super()._url + "/communities"

    def get_community(self, id) -> Community:
        res = requests.get(f"{self.__url}/{id}",
                           headers=self._auth_header,
                           verify=False).json()
        community = TypeAdapter(Community).validate_python(res)
        return community