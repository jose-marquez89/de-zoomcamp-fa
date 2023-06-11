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

## Building first dbt models
- it's possible to write jinja into your dbt sql files
  - you can write functions/macros for more help during compilation
- materialization stragegies
  - there are 4, table and view are most common
    - table
    - view
    - incremental
    - ephemeral
  - if you're an advanced user you can create more

### The FROM clause
- we essentially create a select list
  - data is sourced from our connected DW
- the `FROM` clause, by way of a jinja source macro, will allow us to 
  - resolve to the correct schema
  - define source freshness
- seeds
  - you can essentially load csv files from dbt
  - either a single file or a folder
  - good for data that doesn't change
  - you essentially load these the same way you would do your transformations (`SELECT` statements) except that you use a `ref[]` to point to the csv file(s)
- Ref
  - lets you reference underlying tables and views
  - can use dbt models or dbt seeds
  - you don't need a schema or anything, the keyword resolves everything we need
  - dependencies are built automatically


## Some Misc Notes
Query I used to create external tables:
```sql
CREATE EXTERNAL TABLE `trips_data_all.grn_ext`
OPTIONS (
  format = "PARQUET",
  uris = ['gs://dtc_data_lake_de-zc-i/data/green/green_tripdata_20*.parquet']
);
```

## Development of dbt models
- defining a source
  - use the schema.yml to define a source within the models folder
  - you can later use the schema file to change data sources
- creating models
  - write your transformations in sql files from within the models folder
  - use `dbt run` to create the models in your data warehouse
    - you can run this with specific flags to point at specific transformations
  - you can use jinja and source configuration 

### Macros
- similar to functions
- can use control structures
- you can use environment variables
- you can operate on the results of one query to generate another query
- macros don't necessarily return an object
  - they return code for whatever requirement you've written
- has a DRY benefit (don't repeat yourself)
- `#` is a comment block while `%` denotes a function
  - `{# comment #}`
  - `{% macro macro_name(argument) -%}`
    - `{%- endmacro %}`
- macros are written in .sql files in the macros folder

### Packages
- allows you to bring in macros from other projects
- like libraries in other programming languages
- if you add a package to your project, those macros will become available
- imported in *packages.yml* and brought in by `dbt deps`
- useful packages can be found at the dbt package hub

### Variables
- useful to define values that should be used across the project
- allows us to provide data to models for compilation
- to use a variable we use the `{{ var('...') }}` function
- can be defined in two ways
  - in the dbt_project.yml file
  - on the command line

### Seeds 
- meant to be used with smaller files that will not be changing that often
- so far, the UI does not have an upload feature for the raw files that you might want to put in as seeds
  - for the meantime, you can either push files to your repository or copy/paste into a file in the UI and create the file
- run `dbt seed`
- you can define data types for the seeds in the dbt_project.yml file
- `dbt seed --full-refresh` drops the table and reloads
  - you can do this when there is a change to the dataset and you don't want dbt to carry out normal behaviour (append things that change)

## Testing and documenting the project
- tests in dbt are essentially a select query
- your tests get compiled to sql that returns the amount of failing records
- tests are defined on a colum in the .yml file
- basic tests provided
  - unique
  - not null
  - accepted values
  - foreign key to another table
- you can create your custom tests as queries

### Documentation
- dbt lets you generate documentation and render it as a website. This includes
  - project info
    - model code
    - dependencies
    - sources
    - auto generated dag
    - descriptions from .yaml file
  - info about dw
    - column names and data types
    - table stats like size and rows
    - 
  - docs can be hosted in dbt cloud
- you can use variables in your documentation (which lives in the .yml)
- `dbt test` will just run any tests you created

### Documenting models and columns in the .yml
Below is the basic syntax for model and column documentation in the .yml file.
Variables can be defined in the .yml file. As you can see below, tests are defined
in the same .yml file as well.
```yml
vars:
  payment_type_values: [1, 2, 3, 4, 5, 6]
models:
  - name: name_of_your_model
    description: >
      A long description, perhaps spanning multiple lines
    columns:
      - name: your_first_documented_column
        description: a short description
        tests:
          - unique:
            severity: warn
          - not_null: 
            severity: warn
      - name: your_second_documented_column
        description: a short description about your second column
      - name: third_col
        description: another description
        tests:
          - accepted_values:
            values: "{{ var['payment_type_values'] }}"
            severity: warn
            quote: false
```

## Content checklist
- Intro to analytics engineering
- What is dbt
- Starting a dbt (big query + dbt cloud) 
  - fixed build issue, had to do with bad field names and repeated field names
  - bq doesn't seem to like it when you repeat field names in a select list, even when it comes as a result of a valid join
- Development of dbt models
- TODO: Testing and document dbt models
- TODO: Deploying a dbt project (bq + dbt cloud)
- TODO: Visualizing the transformed data