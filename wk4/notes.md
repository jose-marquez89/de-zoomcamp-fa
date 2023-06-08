# Week 4: Analytics Engineering

## Introduction to Analytics Engineering

### Roles in a Data Team
- DE: prepares and maintains the infrastructure that the data team needs
- Analytics Engineer:
  - fills the gap between the DE and DA
  - introduces good software engineering practices to DE and DA efforts

### AE Tooling
- data loading
- data storage
  - cloud data warehouses like BQ, redshift, snowflake
- data modeling
  - dbt, Dataform
- data presentation
  - looker, mode, tableau, power bi

### Data modeling concepts
- ETL
  - pull data from a source, make some transformations, load it into something like a data warehouse
  - more stable and compliant data due to diligent cleaning
- ELT
  - transform the data once it's in the data warehouse
  - faster and more flexible data analysis 
  - typically lower storage and compute because it takes advantage of cloud data warehouse capabilities like separation of compute and storage

### Some Kimball fundamentals
- main goal: deliver data that the business can use with great performance
- other approaches include: Bill Inmon, data vault
- we're less concerned about 3NF and more inclined to make the data easy to query

#### Elements of dimensional modeling
- fact tables
  - measurements, metrics or facts
  - corresponds to a business process
  - usually verbs
- dimension tables
  - usually corresponds to a business entity
  - provides context to a business process
  - "nouns"

#### The Restaurant Analogy
- stage area: this is where the raw ingredients are
  - not meant to be exposed to the customers
- processing area: this is the kitchen
  - here we take the raw data and make a data model out of it
  - still limited to the people to know how to do this, users do not see this stage
- presentation area:
  - the meal is presented to the guests
  - the data is presented to the business user

## What is dbt?
- a data transformation tool
- allows anyone that knows SQL to deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation
- dbt will be the intermediate step (generally) between the raw data and the transformed version of the data that ends up feeding things like BI tools and other analytics data consuming resources

### How we work with dbt
- develop models
- test and document
- deployment

### How does it work?
- we take data from a data warehouse (like BQ)
- we transform the data
- we feed the data back in to the warehouse
- each model is
  - a sql file
  - select statement with no DDL/DML
  - the file will compile and run in our DW
- seems to compile to some kind of DDL (not sure about this)

### How to use dbt
- dbt Core
  - open source project that allows data transformation
  - builds and runs a dbt project
    - .sql and .yml files
  - includes sql compilation logic, macros and database adapters
  - includes a CLI interface to run commands locally
  - open source and free to use 
- dbt Cloud
  - SaaS application to develop and manage dbt projects 
  - Web based IDE to develop, run and test a dbt project
  - job orchestration
  - logging and alerting
  - integrated documentation
  - free for one developer

### How we'll use dbt
- development using the cloud IDE
- no local installation of dbt core
- our object storage data sources will feed dbt
  - dbt will transform our data
  - transformed data will feed BI dashboard

## Some Misc Notes
Query I used to create external tables:
```sql
CREATE EXTERNAL TABLE `trips_data_all.grn_ext`
OPTIONS (
  format = "PARQUET",
  uris = ['gs://dtc_data_lake_de-zc-i/data/green/green_tripdata_20*.parquet']
);
```

## Content checklist
- Intro to analytics engineering
- What is dbt
- Starting a dbt (big query + dbt cloud) 
- TODO: Development of dbt models
- TODO: Testing and document dbt models
- TODO: Deploying a dbt project (bq + dbt cloud)
- TODO: Visualizing the transformed data