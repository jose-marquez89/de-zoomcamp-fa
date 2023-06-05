# Homework: Wk3

## Question 1:
How many rows across all datasets when loaded into bq?

- 43,244,696 

## Question 2:
Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- 0 bytes on external, ~318 MB on native

## Question 3:
How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?

- 717,748

## Question 4:
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

- Partition by pickup_datetime Cluster on affiliated_base_number

### Answer notes:
- I would not partition by pickup_datetime because it is likely to have many distinct values (high cardinality)

## Question 5:
Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).
Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.

- 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table

### My Query
```sql
CREATE OR REPLACE TABLE trips_data_all.fhv_2019_part_clust
PARTITION BY DATE(pickup_datetime)
CLUSTER BY Affiliated_base_number AS
SELECT *
FROM `trips_data_all.fhv_2019_ext`;
```

```sql
SELECT DISTINCT Affiliated_base_number
FROM `de-zc-i.trips_data_all.fhv_2019_part_clust` 
WHERE pickup_datetime BETWEEN "2019-03-01" AND "2019-03-31";

SELECT DISTINCT Affiliated_base_number
FROM `de-zc-i.trips_data_all.fhv_2019_ext` 
WHERE DATE(pickup_datetime) BETWEEN "2019-03-01" AND "2019-03-31";
```

## Question 6:
Where is the data stored in the External Table you created?

- GCP Bucket

## Question 7:
It is best practice in Big Query to always cluster your data:

- False

## Question 8:
A better format to store these files may be parquet. Create a data pipeline to download the gzip files and convert them into parquet. Upload the files to your GCP Bucket and create an External and BQ Table.

- The files were already set to be written as parquet!