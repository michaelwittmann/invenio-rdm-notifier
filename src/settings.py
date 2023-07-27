from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    invenio_rdm_url: AnyHttpUrl
    invenio_rdm_access_token: str
    slack_webhook_url: AnyHttpUrl
    interval_sec: int = 5
    backup_path: str = "."
