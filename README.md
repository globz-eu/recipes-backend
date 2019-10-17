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
docker run --rm --name recipes-postgres -e APP_USER=$APP_USER -e APP_DB=$APP_DB -e APP_TEST_DB=$APP_TEST_DB -e APP_USER_PASSWORD=$APP_USER_PASSWORD --network recipes-backend -p 5432:5432 -v $PWD/database:/var/lib/postgresql/data -d globz/postgres
```

* Run backend uwsgi

```bash
cd docker
docker build -t globz/recipe-backend .
cd ..
docker run --rm --name recipes-backend --network recipes-backend -e APP_USER=$APP_USER -e APP_DB=$APP_DB -e APP_TEST_DB=$APP_TEST_DB -e APP_USER_PASSWORD=$APP_USER_PASSWORD -p 3031:3031 globz/recipe-backend -r
```

* Collect static

```bash
docker run --rm --name recipes-backend --network recipes-backend -e APP_USER=$APP_USER -e APP_DB=$APP_DB -e APP_TEST_DB=$APP_TEST_DB -e APP_USER_PASSWORD=$APP_USER_PASSWORD -v $PWD/static:/usr/src/app/static -p 3031:3031 globz/recipe-backend -c
```

* Run backend nginx proxy

```bash
docker run --rm --name recipes-backend-nginx --network recipes-backend -p 8000:80 -e "APP_HOST=recipes-backend" -e "APP_PORT=3031" -e "APP_NAME=recipes-backend" -v $PWD/static:/usr/nginx/html/recipes-backend/static globz/nginx-uwsgi-gateway
```
