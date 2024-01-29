import folium
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static

from app.etl.queries import Queries
from app.visualize.helpers import haversine_vectorized

queries = Queries("citibike", "trips")


# Streamlit Layout
def top_bar():
    st.set_page_config(
        page_title="CitiBike Data Analysis", page_icon=":bike:", layout="wide"
    )
    st.title(":bike: CitiBike 2023 Data Analysis And Visualization")
    st.markdown(
        """
    This app provides an interactive way to explore Citibike data.
    You can execute various queries to analyze trip data and visualize the results.
    Visualize or Select a query from the sidebar and provide the necessary inputs to get started.
    """
    )
    total_trips = queries.get_total_trips()
    average_trip_duration = queries.get_average_trip_duration()
    for duration in average_trip_duration:
        avg_duration = round((duration["avg_duration"] / 60000), 2)

    first_column, second_column = st.columns(2)
    with first_column:
        st.subheader("Total Trips Covered")
        st.write(f"{total_trips} trips")

    with second_column:
        st.subheader("Average Trip Duration")
        st.write(f"{avg_duration} minutes")


def sidebar_ops(query_type):
    with st.sidebar:
        st.sidebar.header("Choose a Query")
        query_types = [
            "User Types",
            "Bike Types",
            "Bike Types Used By Members",
            "Popular Stations",
            "Peak Hours",
            "Peak Hours With Day",
            "Total Trips Per Month",
            "Average Trip Duration Per User Types",
            "Average Speed Per User Type and Bike Type",
            "Map Visualization",
        ]
        query_type = st.sidebar.selectbox("Select Query", query_types)

    return query_type
