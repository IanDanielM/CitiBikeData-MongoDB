import streamlit as st
from app.visualize.visualize import (st_user_types,
                                     st_bike_types,
                                     st_bike_types_used_by_members,
                                     st_popular_stations,
                                     st_peak_hours,
                                     st_peak_hours_with_day,
                                     st_average_trip_duration_per_user_types,
                                     st_map_visualization,
                                     st_average_speed_per_user_and_bike_type)
from app.visualize.setup import top_bar, sidebar_ops


def main():
    top_bar()
    data_col, viz_col = st.columns(2)
    query_type = sidebar_ops("visualize")
    if query_type == "User Types":
        st_user_types(data_col, viz_col)
    elif query_type == "Bike Types":
        st_bike_types(data_col, viz_col)
    elif query_type == "Bike Types Used By Members":
        st_bike_types_used_by_members(data_col, viz_col)
    elif query_type == "Popular Stations":
        st_popular_stations(data_col, viz_col)
    elif query_type == "Peak Hours":
        st_peak_hours(data_col, viz_col)
    elif query_type == "Peak Hours With Day":
        st_peak_hours_with_day(data_col, viz_col)
    # elif query_type == "Total Trips Per Month":
    #     st_total_trips_per_month()
    elif query_type == "Average Trip Duration Per User Types":
        st_average_trip_duration_per_user_types(data_col, viz_col)
    elif query_type == "Average Speed Per User Type and Bike Type":
        st_average_speed_per_user_and_bike_type(data_col, viz_col)
    elif query_type == "Map Visualization":
        st_map_visualization()


if __name__ == "__main__":
    main()
