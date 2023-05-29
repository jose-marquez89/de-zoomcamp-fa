# Data Warehouse and Big Query

## Data Warehouse

### Quick review of OLAP vs OLTP
- OLTP
    - productivity: serves the end user
    - revolves around essential biz operations in real time
    - short fast updates initiated by user
    - normalized databases
        - snowflake schema
    - tend to be customer facing, things like online shopping, clerks
- OLAP
    - plan, solve problems, support decisions, discover hidden insights
    - data periodically refreshed with scheduled long running batch jobs
    - denormalized databases
    - generally large to due aggregating nature
    - data analysts, business analysts, executives 

### What is a data warehouse?
- OLAP
- used for reporting and analysis
- generally have a lot of sources
- can be transformed into data marts
    - typically ideal for data analysts
    - data scientists may want to go straight to the data warehouse for raw data
        - maybe to train a model
        - get a better sense of the raw picture

## Big Query
- serverless DW
    - there are no servers to manage
    - no database software to install
- provides software as well as infrastructure
    - scalability and highly available
- some standout built in features
    - ML
    - geospatial analysis
    - BI
- BigQuery separates compute from storage
    - this has huge cost advantages
    - like F of DE says, you have to analyze the specific situation to know if this is going to be the right solution for your org
- uses cached data
    - instructor disabled this to have consistent results

### Costs
- about $5 per 1TB of processing
- there's also flat rate pricing
    - based on a number of prerequested slots
    - 100 slots -> $2000/month = 400TB data processing on demand

### Creating external tables
You can create these from google cloud storage with this kind of query. Quick way to create a table without having to define a schema upfront.
```SQL
CREATE OR REPLACE EXTERNAL TABLE `table-name`
OPTIONS (
    format = 'CSV',
    uris = ['gs://storage/path/to/data-2019-*.csv', 'gs://storage/path/to/data-2020-*.csv']
);
```

### Partitioning
- you can partition a table by a particular column
    - this is similar to indexing in an RDBMS 
- helps to reduce costs when dealing with lots of data
    - the engine won't read things that it doesn't need to
- note: partitioned tables have a different table icon than non-partitioned tables
- the example from the video had about a 93% drop in data read from the non-partitioned to partitioned
    - huge cost advantage!!

Query to create a partitioned table:
```SQL
CREATE OR REPLACE TABLE table_name.partitioned
PARTITION BY
    DATE(datetime_field) AS
SELECT * FROM table_name;
```

You can look directly into partitions (this can be helpful for data mining bias within partitions; some partitions might be noticeably larger than others):
```SQL
SELECT table_name, partition_id, total_rows
FROM your_table.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = your_partitioned_table
ORDER BY total_rows DESC;
```

### Clustering
This is basically partitions within partitions

Here's a query to create this kind of table:
```SQL
CREATE OR REPLACE TABLE table_name_partitioned_clustered
PARTITION BY DATE(datetime_field)
CLUSTER BY VendorID AS 
SELECT * FROM table_name; 
```

*Note: partitioning and clustering are going to give you the most benefit
if you're filtering by whatever you partitioned and clustered by.*

# BQ Best Practices
- cost reduction
    - avoid `SELECT *`
        - specify particular columns
        - there's ways to look at available columns before querying everything
    - price your queries before running them
        - this is especially going to be true with large or long running queries
    - use clustered or partitioned tables
    - use streaming inserts with caution
    - materialize query results in stages
        - if you're using a CTE it might make sense to materialize before you continue
- query performance
    - filter on partitioned columns
    - denormalize data
    - use nested or repeated columns
        - especially true if you have a complicated structure
        - recall that this is what previous unmentioned health company did
    - use external data sources appropriately
        - avoid auto match
    - reduce data before doing a `JOIN`
    - do not treat `WITH` clauses as prepared statements
        - not sure what this means?
    - avoid oversharding tables
        - what does sharding mean?
    - avoid JavaScript UDFs
        - user defined functions
    - use approximation aggregation functions
    - `ORDER` statements should be the last thing in your query
    - optimize your `JOIN` patterns
        - funnel your joins down with the biggest table going first
        - largest table will get distributed evenly
        - second table will get broadcast to all the nodes
            - I assume this has to do with BQ's distributed nature



    

