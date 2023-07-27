# This is a sample Python script.
import logging
import os
import urllib3
from pydantic import ValidationError

from src.notification.slackClient import SlackClient
from src.crawler import DataHubCrawler
from dotenv import load_dotenv, find_dotenv

from src.settings import Settings

urllib3.disable_warnings()
load_dotenv(find_dotenv())
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)



def welcome_message():
    print("""
______   ___  _____  _____  _   _  _   _  _   _ ______         
|  _  \ / _ \|_   _||  ___|| \ | || | | || | | || ___ \        
| | | |/ /_\ \ | |  | |__  |  \| || |_| || | | || |_/ /        
| | | ||  _  | | |  |  __| | . ` ||  _  || | | || ___ \        
| |/ / | | | | | |  | |___ | |\  || | | || |_| || |_/ /        
|___/  \_| |_/ \_/  \____/ \_| \_/\_| |_/ \___/ \____/         
 _____  _       ___   _____  _   __       ______  _____  _____ 
/  ___|| |     / _ \ /  __ \| | / /       | ___ \|  _  ||_   _|
\ `--. | |    / /_\ \| /  \/| |/ / ______ | |_/ /| | | |  | |  
 `--. \| |    |  _  || |    |    \|______|| ___ \| | | |  | |  
/\__/ /| |____| | | || \__/\| |\  \       | |_/ /\ \_/ /  | |  
\____/ \_____/\_| |_/ \____/\_| \_/       \____/  \___/   \_/                                                                 
""")


if __name__ == '__main__':
    welcome_message()

    try:
        settings = Settings()
    except ValidationError as e:
        logging.error("Missing or wrong environment variables:", e)
        exit(1)

    notification_client = SlackClient(Settings().slack_webhook_url.unicode_string())
    crawler = DataHubCrawler(notification_clients=[notification_client])
    crawler.run()
