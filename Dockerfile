FROM python:3.10.12

ENV PYTHONUNBUFFERED 1
RUN mkdir /work
WORKDIR /work

RUN apt-get update && apt-get install -y libopus0
RUN apt-get install -y ffmpeg

ENV OPUS_PATH /usr/lib/x86_64-linux-gnu/libopus.so.0
ENV OS_USERNAME "gncu45473240"
ENV OS_TENANT_NAME "gnct45473240"
ENV OS_PASSWORD "!!Daze2018"
ENV OS_AUTH_URL "https://identity.c3j1.conoha.io/v3"

COPY ./pyproject.toml /work/pyproject.toml

RUN pip install --upgrade pip && pip install poetry
#RUN pip install discord.py typing-extensions
RUN poetry config virtualenvs.create false

COPY . /work
RUN poetry install

CMD [ "poetry", "run", "python", "main.py" ]
