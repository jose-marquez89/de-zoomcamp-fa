from pathlib import Path
from time import time
from datetime import timedelta

import pandas as pd
from prefect import task, flow
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash

# remember that the cache key fn keeps you from having to re-read
# the dataset more than once if it has already been read

# removed the cache_key_fn part because a recent docker failure 
# created some issues with prefect cache storage
# @task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(seconds=30))
@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read data into a pandas df"""
    print(f"Reading file: \n\t{dataset_url}")
    df = pd.read_csv(dataset_url)

    return df

@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtypes in df"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"Column Types: {df.dtypes}")
    print(f"Total Rows: {df.shape[0]}")
    return df

@task()
def write_gcs(path: Path) -> None:
    """Upload the local parquet file to GCS"""
    gcs_bucket = GcsBucket.load("dez-prefect-gcs")
    gcs_bucket.upload_from_path(from_path=f"{path}", to_path=path)

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write dataframe as parquet"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")

    return path

@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """Main ETL function"""
    # TODO: find out what the colon in the last f string parameter does
    # - I've never seen this python feature before
    dataset_file = f"{color}_tripdata_{year}-{month:02}" 
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz" 

    df = fetch(dataset_url)
    if color not in ("green"):
        clean_df = clean(df)
        path = write_local(clean_df, color, dataset_file)
    else:
        path = write_local(df, color, dataset_file)

    write_gcs(path)

@flow()
def etl_parent_flow(months: list[int] = [1, 2], 
                    year: int = 2021,
                    color: str = "yellow") -> None:
    
    for month in months:
        print(f"Running month {month}...")
        etl_web_to_gcs(year, month, color)

if __name__ == "__main__":
    color = "yellow" 
    year = 2021 
    months = [1, 2, 3]
    etl_parent_flow(months, year, color)