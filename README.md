# InvenioRDM Notifier

This project contains a Slack Bot to notify users about new Records added to a InvenioRDM Instance

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

3. Create a docker volume to persist known records
   ```shell
   docker volume create invenio-rdm-notifier-storage
   ```
2. Run docker container
   ```shell
   docker run --mount source=invenio-rdm-notifier-storage,target=/mnt/backup --env-file .env invenio-rdm-notifier:latest 
   ```