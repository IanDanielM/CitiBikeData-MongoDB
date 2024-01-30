import streamlit as st

from app.etl.queries import Queries
from app.visualize.custom_query import CustomQuery
from app.visualize.setup import sidebar_ops, top_bar
from app.visualize.visualize import (
    st_average_speed_per_user_and_bike_type,
    st_average_trip_duration_per_user_types,
    st_bike_types,
    st_bike_types_used_by_members,
    st_peak_hours,
    st_peak_hours_with_day,
    st_popular_stations,
    st_total_trips_per_month,
    st_user_types,
)

st.set_page_config(
    page_title="CitiBike Data Analysis", page_icon=":bike:", layout="wide"
)


def main():
    queries = Queries("citibike", "trips")
    cq_query = CustomQuery("citibike", "trips")

    top_bar(queries)
    data_col, viz_col = st.columns(2)
    query_type = sidebar_ops("visualize")
    if query_type == "Custom Query":
        query = cq_query.custom_query()
        custom_data_df = cq_query.get_custom_query(query)
        cq_query.custom_visualize_data(custom_data_df, data_col, viz_col)
    if query_type == "User Types":
        st_user_types(queries, data_col, viz_col)
    elif query_type == "Bike Types":
        st_bike_types(queries, data_col, viz_col)
    elif query_type == "Bike Types Used By Members":
        st_bike_types_used_by_members(queries, data_col, viz_col)
    elif query_type == "Popular Stations":
        st_popular_stations(queries, data_col, viz_col)
    elif query_type == "Peak Hours":
        st_peak_hours(queries, data_col, viz_col)
    elif query_type == "Peak Hours With Day":
        st_peak_hours_with_day(queries, data_col, viz_col)
    elif query_type == "Total Trips Per Month":
        st_total_trips_per_month(queries, data_col, viz_col)
    elif query_type == "Average Trip Duration Per User Types":
        st_average_trip_duration_per_user_types(queries, data_col, viz_col)
    elif query_type == "Average Speed Per User Type and Bike Type":
        st_average_speed_per_user_and_bike_type(queries, data_col, viz_col)
    elif query_type == "Map Visualization":
        query = cq_query.custom_query()
        map_data_df = cq_query.get_map_query(query)
        cq_query.map_visualize_data(map_data_df)


if __name__ == "__main__":
    main()
