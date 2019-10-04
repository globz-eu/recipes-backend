#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER recipes WITH PASSWORD 'recipesPw';
    CREATE DATABASE recipes;
    GRANT ALL PRIVILEGES ON DATABASE recipes TO recipes;
    CREATE DATABASE test_recipes;
    GRANT ALL PRIVILEGES ON DATABASE test_recipes TO recipes;
EOSQL
