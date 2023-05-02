FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app 
COPY parquet_processing.py parquet_processing.py
ENTRYPOINT ["python", "parquet_processing.py"]