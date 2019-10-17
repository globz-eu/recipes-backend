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

* Build recipes-backend

```bash
cd docker
docker build -t globz/recipes-backend .
```

* Run database with persistent data

```bash
docker run --rm --name recipes-postgres -e APP_USER=$APP_USER -e APP_DB=$APP_DB -e APP_TEST_DB=recipes-test -e APP_USER_PASSWORD=$APP_USER_PASSWORD --network recipes-backend -p 5432:5432 -v $PWD/database:/var/lib/postgresql/data -d globz/postgres
```

* Collect static

```bash
docker run --rm --name recipes-collect-static -e ALLOWED_HOST=$ALLOWED_HOST -e DB_HOST=$DB_HOST -e APP_USER=$APP_USER -e APP_DB=$APP_DB -e APP_USER_PASSWORD=$APP_USER_PASSWORD -v $PWD/static:/usr/src/app/static globz/recipes-backend -c
```

* Run backend uwsgi

```bash
docker run --rm --name recipes-backend --network recipes-backend -e ALLOWED_HOST=$ALLOWED_HOST -e DB_HOST=$DB_HOST -e APP_USER=$APP_USER -e APP_DB=$APP_DB -e APP_USER_PASSWORD=$APP_USER_PASSWORD -p 3031:3031 globz/recipes-backend -r
```

* Run backend nginx proxy

```bash
docker run --rm --name recipes-backend-nginx --network recipes-backend -p 8000:80 -e APP_HOST=$APP_HOST -e APP_PORT=3031 -e APP_NAME=$APP_NAME -v $PWD/static:/usr/nginx/html/recipes-backend/static globz/nginx-uwsgi-gateway
```
