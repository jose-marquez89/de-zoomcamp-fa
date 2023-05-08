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

## Using argparse
Typically, it's much better practice to put your passwords in environment variables or password stores etc. but this is how this particular exercise was carried out for tempo-de-learno:
```

# see the parquet_processing.py script
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet"

python parquet_processing.py \
--user=root \
--password=root \
--host=localhost \
--port=5432 \
--db=ny_taxi \
--table_name=yellow_taxi_trips \
--url=${URL}

```

Build the container that contains the python parquet script:
```
docker build -t taxi-ingest:v001 .
--user=root \
--password=root \
--host=localhost \
--port=5432 \
--db=ny_taxi \
--table_name=yellow_taxi_trips \
--url=${URL}
```

Running the newly built container:
```
docker run -it \
--network=pg-network \
taxi-ingest:v001 \
--user=root \
--password=root \
--host=pg-database \
--port=5432 \
--db=ny_taxi \
--table_name=yellow_taxi_trips \
--url=${URL}
```

# Using Docker Compose
This is convenient way to run related services with one config file
Created the .yaml file in this directory and ran `docker compose up` from within the dir

**Other Stuff**
- The "proper" way to shut the machine down is 'docker compose down' (assuming from the directory it was created)


# SQL Refresher
One way of doing joins:

```SQL
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zp."Borough", ' / ', zp."Borough") AS pu_location,
    CONCAT(zd."Borough", ' / ', zd."Borough") AS do_location
FROM
    yellow_taxi_trips t,
    zones zp,
    zones zd,
WHERE
    t."PULocationID" = zp."LocationID" AND
    t."DOLocationID" = zd."LocationID"
LIMIT 100;
```

Using `JOIN` instead of `WHERE` clause

```SQL
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zp."Borough", ' / ', zp."Borough") AS pu_location,
    CONCAT(zd."Borough", ' / ', zd."Borough") AS do_location
FROM
    yellow_taxi_trips t
JOIN zones zp
	ON t."PULocationID" = zp."LocationID"
JOIN zones zd
    ON t."DOLocationID" = zd."LocationID"
LIMIT 100;
```

A group by feature (in postgres) that I was not aware of:
```SQL
SELECT
    CAST(tpep_dropoff_datetime AS DATE) as "day",
    "DOLocationID",
    COUNT(1) AS "count",
    MAX(total_amount),
    MAX(passenger_count)
FROM
    yellow_taxi_trips t
GROUP BY
    -- looks like you can group by list indices
    -- but not really sure that this is a great practice
    1, 2  
ORDER BY
    "day" ASC,
    "DOLocationID" ASC
```

