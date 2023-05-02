#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd

from sqlalchemy import create_engine

df = pd.read_parquet('data/yellow_tripdata_2021-01.parquet')
df.head()

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

print(pd.io.sql.get_schema(df, name="yellow_taxi_data", con=engine))

df.head(n=0).to_sql(name="yellow_taxi_data", con=engine, if_exists='replace')

df.to_sql(name="yellow_taxi_data", con=engine, if_exists="append")