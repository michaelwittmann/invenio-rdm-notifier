FROM python:3.11-slim
LABEL authors="michael.wittmann@tum.de"
ARG container_user=invenio-rdm-notifier

RUN useradd -m -g users ${container_user}

RUN mkdir /mnt/backup
RUN chmod 770  /mnt/backup

RUN chown ${container_user}:users /mnt/backup


USER ${container_user}

WORKDIR /home/${container_user}/app

ENV PATH="/home/${container_user}/.local/bin:${PATH}"

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src src/
COPY ./main.py .

# if necessary, specify alternative port with --port
CMD ["python", "main.py"]