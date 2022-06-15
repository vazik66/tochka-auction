# Auction
Unviersity project "Auction platform"

## Try
App: https://app.milf-tochka.ru

Docs: https://api.milf-tochka.ru

##  How to start?
```
docker-compose -f docker-compose.traefik.yml up -d
docker-compose -f docker-compose.yml up 
docker exec tochka-auction-web-1 alembic revision --autogenerate -m "init"
docker exec tochka-auction-web-1 alembic upgrade head
```

## What have I learned:
- FastAPI
- RPC
- Caching
- Vue
- Docker
- Traefik
- Github Actions
- How to exit vim

## Possible app improvements:
- Add account balance, because now anyone can bid any amount and not pay
- Add JWT refresh token
- Add email confirmation
- Add multiple workers with gunicorn
- Move constants to config
- Make possibe user to add his wallet so he will get his money 
