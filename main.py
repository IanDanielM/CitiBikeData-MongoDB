import streamlit as st
from etl.extract import ExtractTransformLoad
from etl.queries import Queries
import pandas as pd


queries = Queries("citibike", "trips")

# Streamlit Layout
st.title("Data Visualization with Streamlit")

# Example: Display total trips
if st.button("Show Total Trips"):
    total_trips = queries.get_total_trips()
    st.write(f"Total Trips: {total_trips}")

# Example: Display all data
if st.button("Show All Data"):
    all_data = queries.get_all_data()
    st.write(all_data)

# Example: Visualize some data (adjust according to your data structure)
if st.button("Visualize Data"):
    data = queries.get_all_data()
    df = pd.DataFrame(data)
    # Suppose you have a column 'trip_duration'
    st.line_chart(df["tripduration"])