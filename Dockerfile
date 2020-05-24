FROM python:3.7-slim-stretch
WORKDIR /lifx/
RUN apt -y update && apt -y install curl && apt -y clean && apt -y autoremove 
COPY pyproject.toml poetry.lock /lifx/
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="$PATH:/root/.poetry/bin"
RUN poetry config virtualenvs.create false && poetry install
COPY . /lifx/