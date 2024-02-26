FROM python:3.11.7 AS base

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install pipenv
ENV PATH=/root/.local/share/bin:$PATH
COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --deploy --ignore-pipfile --${PIPENV_ARGS}
COPY .env /app/.env

RUN cat /etc/ssl/certs/ca-certificates.crt >> `python -m certifi`

COPY api/ /app/api

FROM base AS api
COPY asgi.py /app/asgi.py
EXPOSE 8080
CMD ["pipenv", "run","uvicorn", "asgi:api", "--host", "0.0.0.0", "--port", "8080"]

FROM base AS worker
COPY worker/ /app/worker
VOLUME /app/data
CMD ["pipenv", "run", "celery", "-A", "worker.tasks", "worker", "--loglevel=INFO", "-B", "-s", "./data/celerybeat-schedule"]

FROM worker as worker_dev
RUN pip install -U watchdog[watchmedo]
CMD watchmedo auto-restart --directory . --pattern=*.py --recursive -- pipenv run celery -A worker.tasks worker --loglevel=INFO -B -s ./data/celerybeat-schedule

FROM api AS api_dev
CMD ["pipenv", "run", "python3", "asgi.py"]