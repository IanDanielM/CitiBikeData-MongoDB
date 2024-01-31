import os

import streamlit as st

from app.etl.extract import ExtractTransformLoad


def main():
    etl = ExtractTransformLoad("citibike", "trips", uri=st.secrets["URI"])
    base_url = "https://s3.amazonaws.com/tripdata/JC-202301-citibike-tripdata.csv.zip"
    etl.ingest_data(base_url, 2023, "app/etl/data", "trips")


if __name__ == "__main__":
    main()
