# Data Lake vs. Data Warehouse
- what's a data lake?
    - central repository that holds data from many sources
    - all kinds of structures for data
        - semi, un, fully
    - the main idea is quick ingestion
    - used for machine learning and analytics
    - generally needs to be secure
- comparison
    - data lake
        - users: data scientists/analysts
        - lots of big data
        - stream processing, ML, real-time analytics
    - data warehouse
        - users: business analysts
        - data is typicaly structured
        - batch processing, BI reporting  

## How it started 
- companies realized the value of the data that they just had sitting around
- the main idea is to get the data from it's raw form to being useful as quickly as possible
    - we don't wait to determine relationships and things like referential integrity here as we do in a DW
- because data tends to be more useful in the later stages of a project, companies sought to put data into a stored form as soon as possible
    - this came down to storing the data as cheaply as possible

## ETL vs ELT
- the export and load steps are flipped around
- ELT is something we tend to favor when working with quite large amounts of data
- as opposed to ETL processes, ELT is *schema on read*
    - we write the data first and the determine schema upon reading

## Gotchas
- can be well intentioned
    - turns into a data swamp
    - different data/file types can make things difficult to use
- there's no versioning
- no metadata
- can't really join (unless there's some kind of other infrastructure that runs on top of the data lake)
    - note to self: thinking maybe delta lake or hudi tables?
    - what are these, do these make a difference in cases like this?
    - what's the technical overhead and does it make more sense to work with a DW
        - probably depends on size of data

## Cloud providers
- GCP: cloud storage
- AWS: S3
- Azure: Azure Blob

# Intro to Workflow Orchestration
- workflow orchestration allows you to turn any code into a workflow that you can
    - schedule
    - run
    - observe
- basically this is the same idea behind SSIS
- think of it as a well designed and robust delivery system
- all about dataflow and reliable execution
    - should respect your privacy
    - should give you some insight into how things went
        - think tracking (logging, errors etc)
- a good workflow orchestration tool should allow you to orchestrate a wide range of data processes and tools
- existing tools
    - prefect
    - airflow
    - luigi
    - cron
    - dagster
    - a few others

# Intro to Prefect concepts
We're going to create a new ingest script.

```bash
export URL="https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2023-01.parquet"

python pq_process_simple.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=for_hire_vehicle_trips \
    --url=${URL}
```

## Parameterization and subflows
I didn't do this within `pq_process_simple.py` because it didn't make sense with the argument parser, but here are some notes about this nonetheless:

When you do the following, you'll see that a new subflow will be announced in stdio.

```python
@flow(name="subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f"Logging subflow for: {table_name}")

@flow(name="Ingest Flow")
def main_flow(table_name: str):
    # code
    # code

    # here we call the subflow
    log_subflow(table_name)

    # code
    # code
```

## Running the Orion UI
Remember to set the URL for the UI:
```shell
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

To run: `prefect orion start`


## Blocks
Blocks securely store credentials and configuration to easily manage connections to external systems.

Blocks enable storage configuration. Provides a central location. Kinda like modular connectors. Block names are immutable.
- blocks can be pip installed from something like a repository of connectors
- you can use these within your code instead of things like postgres connection strings
- you set the parameters in the UI
    - post, dbname, etc (all the stuff you would normally use in a connection string)

Example:
```python
from prefect_sqlalchemy import SqlAlchemyConnector

with SqlAlchemyConnector.load("<name-of-your-block>") as database_block:
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    df.to_sql(name=table_name, con=engine, if_exists="append")
```

Alternatively you can put `SqlAlchemyConnector.load("block-name")` into a variable and use that after the `with` keyword.

## Some notes to self
These were taken during prefect walkthrough:
- you can't run a task (`@task` decorated functions) within other tasks

# Prefect to GCP ETL
Steps for using blocks:
1. register blocks
2. select a block for use and name it
3. add credentials from a service account with the appropriate permissions

See *etl_web_to_gcp.py*

## Registering a block
Run the following to register a block (not sure what this means or what it is for though)

Seems to display a new set of registered blocks.
```shell
prefect block register -m prefect_gcp
```

# Prefect GCS to BQ
Steps to create a dataset in BQ and add data
1. hit the "ADD+" button
2. create a new dataset and give it a unique name
3. give the incoming data a table name 
4. if there's no partitioning to be done, go ahead and create the table