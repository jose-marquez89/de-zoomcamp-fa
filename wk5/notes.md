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

## Creating a Local Spark Cluster
Documentation for starting a cluster manually is [here](https://spark.apache.org/docs/latest/spark-standalone.html)

- go to your `$SPARK_HOME` directory
- run the `sbin/start-master.sh` script
- the spark cluster should be running at port 8080
- you can connect your spark session to the running spark cluster by setting the `.master()` method argument to the spark cluster URL like so
    - `.master("spark://jose-MacBookPro:7077")`
    - this could be a locally hosted cluster (as above) or a cluster hosted at another URL
        - this is a networking thing
- if you see this message, you haven't set up any workers:
    - "WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources"
    - you can start one or more workers and connect them to the master with `sbin/start-worker.sh <master-spark-URL>`

### Spark-Submit
Spark-submit is a script that comes with spark that you can use to submit jobs to spark clusters
- hard coding the master (the main cluster) is not very practical if you want to use a script with something like airflow for example

What it looks like in a simple local example for PySpark (Java and Scala will have their own versions, see the [spark docs](https://spark.apache.org/docs/latest/submitting-applications.html))
```shell
CR_URL="spark://jose-MacBookPro:7077"

spark-submit \
    --master "${CR_URL}" \
    local_spark.py \
        --input_green=data/pq/green/2020/*/ \
        --input_yellow=data/pq/yellow/2020/*/ \
        --output=data/report-2020
```

### Other stuff
- convert your notebooks to scripts in the terminal using `juypter nbconvert to=script <notebook_name.ipynb>`
- if a notebook or script cannot access any workers, it could be that you are taking them up with another script
    - you can kill the offending applications on the spark cluster UI
- checking dates of files in the terminal
    - `ls -lg` will produce permissions and dates (maybe other stuff too?)
- if you've started your spark cluster manually, when you're done with spark, you need to stop the master and workers
    - in your Spark executables directory
    - `./sbin/stop-worker.sh`
    - `./sbin/stop-master.sh`

## Setting up a Dataproc Cluster
- a dataprocessing cluster
    - "managed hadoop clusters in gcp"
- to start, search 'dataproc' in GCP
    - you'll need to enable the dataproc API
    - once you're done, create a cluster in your desired region
    - the cluster type will only matter in a real project
        - for the mean time, a single node cluster is fine (0 workers)

### Submitting a job
- go to the cluster
- choose a job type (hadoop, spark, pyspark, etc)
- upload your code to somewhere in your data lake
    - from code dir: `gsutil cp local_spark.py gs://dtc_data_lake_de-zc-i/code/`

While this is a convenient way to submit a one-off job, this isn't the path you would take if you were trying to use an orchestration tool or the command line. In that case you would probably want to work with a REST api. This is described in more detail below:

### Using an API to submit a job
- you can submit a job via three different methods
    - REST API
    - GCP SDK
    - Web UI
    - see more at the [docs](https://cloud.google.com/dataproc/docs/guides/submit-job#dataproc-submit-job-gcloud)
- this is more helpful when using the command line or an orchestration tool like Airflow
- ideally you have different roles for your orchestration tool but here we kept things simple and just used our main service account

The equivalent gcloud command (yes you do seem to need the stray `--` for the pyspark job args):
```shell
gcloud dataproc jobs submit pyspark \
    --cluster=de-zc-cluster \
    --region=europe-west6 \
    gs://dtc_data_lake_de-zc-i/code/local_spark.py \
    -- \
    	--input_green=gs://dtc_data_lake_de-zc-i/pq/green/2021/*/ \
        --input_yellow=gs://dtc_data_lake_de-zc-i/pq/yellow/2021/*/ \
        --output=gs://dtc_data_lake_de-zc-i/report-2021/ 
```

## Connecting Spark to BigQuery
- change the last line of the *local_spark.py* file to write to a bigquery table instead of a parquet file in GCS

The CLI command will change just slightly (the `--output` flag will have a big query table instead of a gcs path and we'll use a different python file)
```shell
gcloud dataproc jobs submit pyspark \
    --cluster=de-zc-cluster \
    --region=europe-west6 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://dtc_data_lake_de-zc-i/code/gcs_spark_big_query.py \
    -- \
    	--input_green=gs://dtc_data_lake_de-zc-i/pq/green/2020/*/ \
        --input_yellow=gs://dtc_data_lake_de-zc-i/pq/yellow/2020/*/ \
        --output=trips_data_all.report_2020 
```

### Recap
What did we do here?
- we used a dataproc (gcp managed hadoop cluster) to process spark jobs that resulted in either of a write to parquet files in gcs or a table in big query