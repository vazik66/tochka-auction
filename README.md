# Tochka auction project

##  How to start ?
```
docker-compose up --build
docker exec container_name alembic revision --autogenerate -m "init"
docker exec container_name alembic upgrade head
```
