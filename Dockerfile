FROM python:3.11-slim
LABEL authors="michael.wittmann@tum.de"
ARG container_user=datahub-slack-bot

RUN useradd -m -g users ${container_user}
USER ${container_user}

WORKDIR /home/${container_user}/app

ENV PATH="/home/${container_user}/.local/bin:${PATH}"

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src src/
COPY ./main.py .

# if necessary, specify alternative port with --port
CMD ["python", "main.py"]