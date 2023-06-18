# Batch processing with Spark

## Some definitions
- batch processing
    - basically a batch from a particular date or some range of dates
    - big chunks of data in one go
    - most typically daily and hourly
- streaming
    - taxi example
        - rider hops in taxi
        - taxi driver's electronic device sends message (`RIDE_STARTS` perhaps?) to data stream
        - data stream is sent to processor for...processing
        - processed data is sent to another stream

## Technologies
- python scripts
- SQL
- Spark
- Flink, others
- usually orchestrated with something like Airflow
- a typical batch workflow
    - data lake csv -> python processing -> sql (dbt) -> spark -> perhaps some more processing with python

## Advantages
- easy to manage
    - workflow tools that make it easy to parameterize (parametrize?)
- easy to retry
- scale

## Disadantages
- delay
    - on top of data freshness, you also have processing time that adds to the lag
- usually this does not outweigh the advantages
- not usually a deal breaker to not have data down to the minute

## Apache Spark
- an open source unified analytics engine for large-scale data processing
- distributed engine
    - this might process data from a data lake and then put it back in a DW
    - all the while the processing can be distributed across many machines
- multi-language
    - Java
    - Python (pyspark)
    - Scala
- batch but can be used for streaming
    - streaming is usually a sequence of small batches in this scenario

## When to use Spark
- if you can express your batch job as SQL, go with Hive/Presto/Athena
- if you need more modularity, testing or the batch job is just not as easy to express using sql (versus code), use something like spark
    - often used for things like machine learning where it's just a bit harder to express necessary transformations/processes as sql

## Some spark internals basics
- spark basically uses different machines for each file (called a partition)
- the ideal situation is having many small partitions that are being worked on by individual machines
    - when there is just one large partition, one worker must handle this while others remain idle
    - this is not a good use of spark
    - break the file up into smaller partitions
- when a machine is done with a partition, it will move on to another
- the `.repartition(amount_of_partitions)` method will split the current dataframe up into an amount of partitions that you want
    - lazy, doesn't do anything until you write to a file
    - expensive operation

## Spark DataFrames
- there are actions and transformations
    - transformations are lazy
    - actions are when transformations are actually executed
        - `.show()`, `.take()`, `.head()`, `.write()` are actions
        - `.filter()` or `.where()` is a transformation

## Anatomy of a Spark Cluster
- when you set up a local cluster, this is when you use `local[*]`
- flow
    - you write your code somewhere, like on your computer
    - the code is submitted to a spark cluster which has a master machine
        - usually at port 4040
        - the master will coordinate the processing of a job using available executors
        - executors pull from a partitioned dataframe
            - usually live in s3 or cloud storage
            - also hadoop/hdfs
                - this used to provide the advantage that the executor would operate on data that was local to it
                - (for) now the preferred way is to just use cloud storage because the cloud providers have their own internal networks

## Spark implementation of group by
- a group by is implemented (usually) in three stages, which are visible in the DAG part of the UI
    - it's assumed that you're using an order by in your query
    - a preparatory stage
    - the actual group by
    - an order by
- each executor will operate on its respective part of the dataset
    - filter ->
    - group by
    - recall that each executor can only work on one partition at a time
- the second stage
    - contains intermediate results
    - each intermediate result from each executor is combined 
    - this is where reshuffling occurs
        - external merge sort occurs here
        - keyed result rows in each intermediate result are sent to corresponding partitions
- the external merge sort will combine everything into the final result
- if you do an order by, you will add a stage that orders everything
- sidenote regarding the partitions you end up with at the end of a query (which can be seen in the UI)
    - if your files are small, it's better to repartition to have less partitions
    - if your files are quite large, many smaller partitions will be ideal
- try not to do too much reshuffling
    - it's expensive
- the tasks column of the UI corresponds to partitions

## Spark implementation of Joins
- the example join is carried out on the yellow and green datasets
    - joined on 2 columns and adding 2 from each table for a total of 6 columns
- how it works
    - each table is split into sections (partitions maybe?) composed of partitions
    - a new record type based on keys is created
        - the key is a representation of a unique column record combination
    - the keys are used in a reshuffling stage in which records associated with keys are organized into respective partitions
    - an external merge sort occurs (called SortMergeJoin in the UI)
        - keys are used to combine records from each table (yellow/green)
        - record combination behavior will be different depending on what kind of join you've chosen to implement
- sidenote on writing
    - it can be good practice to "materialize" (that shouldn't really be in quotes but it's a reference to SQL/RDBMS) results into partitioned files
    - this will make it easier/faster to perform joins/group by's, and has the added benefit that the table can be used for anoter process
- when one table is large and the other is small
    - instead of the usual partitioning of each larger table into records
        - each executor operates on:
            - a partition of the large table
            - a copy of the smaller table
                - this is known as broadcasting
                - no shuffling is done in this stage

## Connecting to Google Cloud Storage
We ran the command below to upload our parquet folder to gcs:
```shell
gsutil -m cp -r pq/ gs://dtc_data_lake_de-zc-i/pq
```