import pytest

from src.crawler import DataHubCrawler


class TestCrawler():
    def test_check_for_new_records(self):
        crawler = DataHubCrawler()
        records = crawler.fetch_newest_records()
        assert records


