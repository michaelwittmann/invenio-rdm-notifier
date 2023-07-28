import abc
import logging

from src.invenio_rdm_datamodel import Record, RecordAPI, UserAPI, User, CommunityAPI, Community
import re
import markdownify

CLEANER = re.compile('<.*?>')


class NotificationClient(abc.ABC):

    @staticmethod
    def clean_html_str(string: str):
        return re.sub(CLEANER, ' ', string).strip()

    @staticmethod
    def str_to_markdown(string: str):
        return markdownify.markdownify(string)

    @staticmethod
    def shorten_string(string: str, n=500):
        return (string[:n] + '...') if len(string) > n else string

    @abc.abstractmethod
    def notify_new_record(self, record: Record):
        raise NotImplementedError

    @abc.abstractmethod
    def notify_updated_record(self, record: Record):
        raise NotImplementedError

    @staticmethod
    def get_publisher_for_record(record: Record) -> str:
        try:
            if owned_by := next(iter(record.parent.access.owned_by), None):
                user = UserAPI().get_user(owned_by.user)
                if user:
                    if user.profile.full_name:
                        return user.profile.full_name
                    if user.username:
                        return user.username
        except Exception as e:
            logging.error(e)
        if record.metadata.publisher:
            return record.metadata.publisher

        return "Anonymous"

    @staticmethod
    def get_community_for_record(record: Record) -> str | None:
        try:
            if community_id := record.parent.communities.default:
                community = CommunityAPI().get_community(community_id)
                return community.metadata.title
        except Exception as e:
            logging.error(e)
        return None
