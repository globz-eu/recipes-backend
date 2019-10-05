# Recipes Backend

Backend for [Recipes](https://github.com/globz-eu/recipes)

## Development setup

* Setup database

```bash
docker run --rm --name recipes_postgres -e POSTGRES_PASSWORD=postgresPw -it -p 5432:5432 -v $PWD/init-user-db.sh:/docker-entrypoint-initdb.d/init-user-db.sh -d postgres
```

* Setup database with persistent data

```bash
docker run --rm --name recipes_postgres -e POSTGRES_PASSWORD=postgresPw -it -p 5432:5432 -v $PWD/init-user-db.sh:/docker-entrypoint-initdb.d/init-user-db.sh -v $PWD/database:/var/lib/postgresql/data -d postgres
```
