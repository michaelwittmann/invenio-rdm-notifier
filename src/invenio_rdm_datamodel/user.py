import requests
from pydantic import BaseModel, TypeAdapter, EmailStr

from src.invenio_rdm_datamodel.api import InvenioRDMAPI


class Profile(BaseModel):
    full_name: str | None = ""
    affiliations: str | None = ""


class User(BaseModel):
    id: int
    revision_id: int
    username: str
    email: EmailStr
    profile: Profile


class UserAPI(InvenioRDMAPI):
    @property
    def __url(self):
        return super()._url + "/users"

    def get_user(self, id: int) -> User:
        res = requests.get(f"{self.__url}/{id}",
                           headers=self._auth_header,
                           verify=False).json()
        user = TypeAdapter(User).validate_python(res)
        return user
