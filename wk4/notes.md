# Week 4: Analytics Engineering

## Some Misc Notes
Query I used to create external tables:
```sql
CREATE EXTERNAL TABLE `trips_data_all.grn_ext`
OPTIONS (
  format = "PARQUET",
  uris = ['gs://dtc_data_lake_de-zc-i/data/green/green_tripdata_20*.parquet']
);
```

TODO: check if everything worked with dbt