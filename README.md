# Tochka auction project

##  How to start ?
```
docker-compose up --build
docker exec container_name alembic --autogenerate -m "init"
docker exec container_name alembic upgrade head
```
