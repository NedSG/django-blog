# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.3
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/app
ENV APP_HOME=/app/blog

WORKDIR $HOME

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY ./entrypoint.sh $HOME
RUN chmod +x $HOME/entrypoint.sh
COPY . $HOME

RUN mkdir $HOME/static

RUN chown -R appuser $HOME

USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]
