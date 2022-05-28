# Tochka auction project

##  How to start ?
```
docker-compose -f docker-compose.traefik.yml up -d
docker-compose -f docker-compose.yml up 
docker exec container_name alembic --autogenerate -m "init"
docker exec container_name alembic upgrade head
```
