FROM python:3.10.12

ENV PYTHONUNBUFFERED 1
RUN mkdir /work
WORKDIR /work

RUN apt-get update && apt-get install -y libopus0
ENV OPUS_PATH /usr/lib/x86_64-linux-gnu/libopus.so.0

COPY ./pyproject.toml /work/pyproject.toml

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

COPY . /work
RUN poetry install

EXPOSE 5000
CMD [ "poetry", "run", "python", "main.py" ]
