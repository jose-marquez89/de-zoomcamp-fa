from pathlib import Path
import pandas as pd
from prefect import task, flow
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from gcs"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("dez-prefect-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path="data")

    return Path(f"data/{gcs_path}")

@task()
def transform(path: Path) -> pd.DataFrame:
    """Simple data cleaning"""
    df = pd.read_parquet(path)
    print(f"Reading file at: {path}")
    print(f"File Row Count: {df.shape[0]}")
    print(f"Missing passenger (pre): {df['passenger_count'].isna().sum()}")
    df["passenger_count"] = df['passenger_count'].fillna(0)
    print(f"Missing passenger (post): {df['passenger_count'].isna().sum()}")

    return df

@flow()
def etl_gcs_to_bq():
    """Main ETL to load data into Big Query"""
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)

if __name__ == "__main__":
    etl_gcs_to_bq()