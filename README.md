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
docker run --rm --name recipes-backend --network recipes-backend -v $PWD:/usr/src/app -p 3031:3031 globz/django-runner
```

* Collect static

```bash
python manage.py collectstatic --noinput
```

* Run backend nginx proxy

```bash
docker run --rm --name recipes-backend-nginx --network recipes-backend -p 8000:80 -e "APP_HOST=recipes-backend" -e "APP_PORT=3031" -e "APP_NAME=recipes-backend" -v $PWD/static:/usr/nginx/html/recipes-backend/static globz/nginx-uwsgi-gateway
```
