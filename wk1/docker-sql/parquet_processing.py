#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import pandas as pd

from sqlalchemy import create_engine

def load_data(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name 
    url = params.url
    parquet_fname = "data/pq_out.parquet"

    os.system(f"wget {url} -O {parquet_fname}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df = pd.read_parquet(parquet_fname)
    pd.io.sql.get_schema(df, name=table_name, con=engine)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    df.to_sql(name=table_name, con=engine, if_exists="append")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest parquet data into postgres db")
    
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres user')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port on which postgres is running')
    parser.add_argument('--db', help='target database name')
    parser.add_argument('--table_name', help='database table name')
    parser.add_argument('--url', help='url of the file')

    args = parser.parse_args()

    load_data(args)
    