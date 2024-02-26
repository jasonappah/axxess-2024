## Gia API
A RestAPI real world app based on SQLModel [documentation example](https://sqlmodel.tiangolo.com/tutorial/), using [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/)


### Quickstart
Ensure you have Pipenv installed before continuing: https://pipenv.pypa.io/en/latest/#install-pipenv-today

1. **Install dependencies locally (for type checking)**: `pipenv install`
2. **Start API with required services**
   a. **Dev mode**: `docker compose -f docker-compose.yml -f docker-compose.dev.yml up`
   b. **Prod mode**: `docker compose -f docker-compose.yml up`
3. **Explore API documentation**: `http://localhost:8080/#/`

