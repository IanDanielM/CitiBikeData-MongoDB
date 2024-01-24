import streamlit as st
from app.etl.extract import ExtractTransformLoad
from app.etl.queries import Queries
import pandas as pd


etl = ExtractTransformLoad("citibike", "trips")
base_url = "https://s3.amazonaws.com/tripdata/JC-202301-citibike-tripdata.csv.zip"
etl.ingest_data(base_url, 2023, "app/etl/data", "trips")
queries = Queries("citibike", "trips")
data = queries.aggregate_by_birth_year_and_gender()
for data in data:
    print(data)
