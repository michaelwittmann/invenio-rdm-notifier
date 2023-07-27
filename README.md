# InvenioRDM Notifier

This project contains a Bot to notify users about new Records added to a InvenioRDM Instance
Currently, only Slack is supported as a notification channel, others may follow. Feel free to contribute!

# Getting started

## Python

1. Install `requirements.txt`
    ```shell
    pip install -r requirements.txt
    ```
2. Set Environment variables
   ```shell
    # Required
    export INVENIO_RDM_URL=<INVENIO_RDM_URL>
    export INVENIO_RDM_TOKEN=<INVENIO_RDM_TOKEN>
    export SLACK_WEBHOOK_URL=<SLACK_WEBHOOK_URL>
    
    # Optional
    export INTERVAL_SEC=60
    export BACKUP_PATH=.
   ```
   or use an `.env` file
   ```
   cp .env-dev .env
   ```
3. Run InvenioRDM Notifier
   ```shell
   python main.py
   ```

## Docker
1. Build docker image
   ```shell
   docker build -t invenio-rdm-notifier:latest .
   ```
2. Setup environment variables
   ```shell
   cp env-dev .env
   nano .env
   ```
   
2. Run docker container
   ```shell
   docker run --env-file .env invenio-rdm-notifier:latest 
   ```
