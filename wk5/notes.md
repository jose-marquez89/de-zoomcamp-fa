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

