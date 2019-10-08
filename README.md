# Recipes Backend

Backend for [Recipes](https://github.com/globz-eu/recipes)

## Development setup

* Setup database

```bash
docker run --rm --name recipes_postgres -e POSTGRES_PASSWORD=postgresPw -it -p 5432:5432 -v $PWD/init-user-db.sh:/docker-entrypoint-initdb.d/init-user-db.sh -d postgres
```

## Run backend

* Create Docker network

```bash
docker network create recipes-backend
```

* Run database with persistent data

```bash
docker run --rm --name recipes-postgres -e POSTGRES_PASSWORD=postgresPw --network recipes-backend -p 5432:5432 -v $PWD/init-user-db.sh:/docker-entrypoint-initdb.d/init-user-db.sh -v $PWD/database:/var/lib/postgresql/data -d postgres
```

* Run backend uwsgi

```bash
docker build docker/recipes/. -t globz/recipes-backend
docker run --rm --name recipes-backend --network recipes-backend -v $PWD:/usr/src/app -p 3031:3031 globz/recipes-backend
```

* Run backend nginx proxy

```bash
docker build docker/nginx/. -t recipes-backend-nginx
docker run --rm --name recipes-backend-nginx --network recipes-backend -p 8000:80 -v $PWD/static:/usr/nginx/html/recipes-backend/static recipes-backend-nginx
```
