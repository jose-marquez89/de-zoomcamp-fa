#!/usr/bin/env python

"""
This is basically just a copy of the code in wk1: docker-sql
"""

import argparse
import os
import pandas as pd
import pyarrow.parquet as pq
from time import time
from datetime import timedelta

from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash

# tasks not required for flows but can receive data about upstream dependencies
# and the state of those dependencies before the function is run
# retries: the number of times to retry the function before calling it quits
# cache_key_fn: allows you to cache computationally intensive functions 
@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(params, pfname):
    url = params.url
    os.system(f"wget {url} -O {pfname}")


def transform_chunk(df):
    df["PUlocationID"] = df["PUlocationID"].fillna(-99)
    df["DOlocationID"] = df["DOlocationID"].fillna(-99)

    return df


@task(log_prints=True, retries=3)
def load_data(params, pfname):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name 

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    pfile = pq.ParquetFile(pfname)
    bcount = 1

    for batch in pfile.iter_batches():
        print(f"Working on batch {bcount}")
        bdf = batch.to_pandas()

        if bcount == 1:
            bdf.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
        
        bdf_trans = transform_chunk(bdf)
        
        bdf_trans.to_sql(name=table_name, con=engine, if_exists="append")
        bcount += 1

    print(f"Completed table data loaded to {table_name}")

@flow(name="Ingest Flow")
def main():
    parser = argparse.ArgumentParser(description="Ingest parquet data into postgres db")
    
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres user')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port on which postgres is running')
    parser.add_argument('--db', help='target database name')
    parser.add_argument('--table_name', help='database table name')
    parser.add_argument('--url', help='url of the file')

    args = parser.parse_args()
    parquet_fname = "data/pq_out.parquet"

    extract_data(args, parquet_fname)
    load_data(args, parquet_fname)

if __name__ == "__main__":
    # TODO: parameterization and sub flows
    main()
