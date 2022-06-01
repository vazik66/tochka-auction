# Tochka auction project

##  How to start ?
```
docker-compose -f docker-compose.traefik.yml up -d
docker-compose -f docker-compose.yml up 
docker exec tochka-auction-web-1 alembic --autogenerate -m "init"
docker exec tochka-auction-web-1 alembic upgrade head
```
