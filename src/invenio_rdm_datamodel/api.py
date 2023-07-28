from src.settings import Settings


class InvenioRDMAPI:

    @property
    def _url(self):
        return f"{Settings().invenio_rdm_url}/api"

    @property
    def _token(self):
        return Settings().invenio_rdm_access_token

    @property
    def _auth_header(self):
        return {"Authorization": f"Bearer {self._token}"}

