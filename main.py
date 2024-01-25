import streamlit as st
from app.etl.extract import ExtractTransformLoad
from app.etl.queries import Queries
import pandas as pd


queries = Queries("citibike", "trips")
data = queries.get_peak_usage_hours()
for data in data:
    print(data)
