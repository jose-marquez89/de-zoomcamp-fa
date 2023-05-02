# General Notes

To start a python container from a bash entry point
```
docker run -it --entrypoint=bash python:3.9
```

To build a container from a Dockerfile in the current working dir:
```
docker build -t test:pandas .
```

To run a container with arguments passed to the internal pipeline program:
```
docker run -it test:pandas <some_argument>
```

*Use double quotes with JSON(?) arrays in docker file*

Getting the first 100 rows of a CSV:
```
head -n 100 <file>
```

Count lines in a file (not sure if this works for CSV)
```
wc -l <file>
```

### Connecting to postgres in docker

Run postgres server in container from image (you must have a network created for the network flags)
```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13
```

Connect to running database with pgcli
```
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

At some point I realized I just randomly mapped my postgres database volume to
some unknown part of my drive. You have the option in docker to list volumes like so:
```
docker volume ls
```

You can also inspect a specific volume
```
docker volume inspect ny_taxi_postgres_data
```

...and finally, if you want to remove the volume, it's as easy as
```
docker volume rm <your-volume-name>
```

## Steps in loading data to posgres container
- create a postgres container image
- start the posgres server
    - map data volume to local drive to persist data
- load data from a python script into newly created schema

# Connecting PgAdmin and Postgres
Putting multiple containers in one network:
```
# first stop any running containers (the ones that will be in your network)
docker network create pg-network

# ensure that you add the --network and --name flags to the run commands
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin \
dpage/pgadmin4
```

*Remember to use the database --name flag attribute as the host name in pg admin to be able to connect!*

# Dockerizing the Ingestion Script
Converting jupyter notebooks to python scripts
```
jupyter nbconvert --to=script Reading_NY_TAXI_Parquet.ipynb
```
