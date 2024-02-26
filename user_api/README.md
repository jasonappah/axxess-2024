## Gia API
A RestAPI real world app based on SQLModel [documentation example](https://sqlmodel.tiangolo.com/tutorial/), using [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/)


### Quickstart
Ensure you have Pipenv installed before continuing: https://pipenv.pypa.io/en/latest/#install-pipenv-today

1. **Install dependencies**: `pipenv install`
2. **Run PostgreSQL, Redis, and SuperTokens Core**: `docker compose up`
3. **Start the API**: `pipenv run python asgi.py`
4. **Run Celery Worker**: pipenv run celery -A worker.tasks worker --loglevel=INFO -B -s ./data/celerybeat-schedule
5. **Explore API documentation**: `http://localhost:8080/#/`

