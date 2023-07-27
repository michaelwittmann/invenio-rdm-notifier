import abc

from src.record import Record
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
