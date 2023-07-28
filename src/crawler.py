import logging
import os
import time
from typing import List
import pickle
from pathlib import Path
import requests
import schedule
from pydantic import TypeAdapter

from src.invenio_rdm_datamodel import Record, RecordAPI
from src.notification.notificationClient import NotificationClient
from src.settings import Settings


class DataHubCrawler:
    known_record_ids: set
    notificationClients: List[NotificationClient] = []

    @property
    def __backup_path(self):
        return Path(Settings().backup_path)

    @property
    def interval(self) -> int:
        return int(os.environ.get('INTERVAL_SEC', '10'))

    def __init__(self, notification_clients=None):
        self.restore_known_records()
        if notification_clients:
            self.notificationClients = notification_clients

    def run(self):
        schedule.every(self.interval).seconds.do(self.check_for_new_records)
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                logging.error("Error while checking for new records", e)

    def check_for_new_records(self) -> None:
        # 1. Fetch new records
        records = RecordAPI().get_newest_records(50)
        fetched_ids = {record.id for record in records if record.status == "published"}

        # 2. Compare with already known records
        new_ids = fetched_ids - self.known_record_ids
        self.known_record_ids.update(fetched_ids)
        self.save_known_record_ids()

        # 3. Create Notification for new records
        for record_id in new_ids:
            record = next((record for record in records if record.id == record_id), None)
            self.send_notification(record)

    def send_notification(self, record: Record):
        if record.versions.index == 1:
            for notification_client in self.notificationClients:
                logging.info(f"Sending new record notification for record {record.id} at {notification_client.__class__.__name__}")
                notification_client.notify_new_record(record)
        else:
            for notification_client in self.notificationClients:
                logging.info(f"Sending updated record notification for record {record.id} at {notification_client.__class__.__name__}")
                notification_client.notify_updated_record(record)

    def restore_known_records(self):
        self.known_record_ids = set()
        back_up_file = self.__backup_path.joinpath("known_ids.bak")

        if back_up_file.exists():
            try:
                with open(self.__backup_path.joinpath("known_ids.bak"), "rb") as f:
                    self.known_record_ids = pickle.load(f)
                    logging.info("Restored know records")
            except Exception as e:
                logging.error("Could not restore known records from backup", e)
        else:
            logging.warning("Could not find file to restore known records from backup")

    def save_known_record_ids(self):
        try:
            with open(self.__backup_path.joinpath("known_ids.bak"), "wb") as f:
                pickle.dump(self.known_record_ids, f)
                logging.info("Persisted known records")
        except Exception as e:
            logging.error("Could not persist known records", e)
