import streamlit as st
from etl.queries import Queries
import pandas as pd
import datetime
import plotly.express as px


queries = Queries("citibike", "trips")

# Streamlit Layout
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


with st.sidebar:
    st.sidebar.header("Choose a Query")
    query_type = st.sidebar.selectbox(
        "Select Query",
        [
            "User Types",
            "Bike Types",
            "Bike Types Used By Members",
            "Popular Stations",
            "Average trip duration per user types",
            "Peak Hours",
            "Peak Hours With Day",
            "Total Trips Per Month",
        ],
    )

data_col, viz_col = st.columns(2)

if query_type == "User Types":
    user_types = queries.count_by_user_type()
    user_types_list = list(user_types)
    user_types_df = pd.DataFrame(user_types_list, columns=["count", "usertype"])
    with data_col:
        st.caption("User Types Data")
        st.dataframe(user_types_df, use_container_width=True, hide_index=True)
    with viz_col:
        fig = px.pie(
            user_types_df,
            values="count",
            names="usertype",
            title="User Types Visualization",
            color="usertype",
            color_discrete_map={"customer": "#FFA500", "member": "#0000FF"},
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

elif query_type == "Bike Types":
    bike_types = queries.bike_count()
    bike_types_list = list(bike_types)
    bike_types_df = pd.DataFrame(bike_types_list, columns=["count", "bike type"])
    with data_col:
        st.caption("Bike Types Data")
        st.dataframe(
            bike_types_df,
            use_container_width=True,
            hide_index=True,
            column_order=["bike type", "count"],
        )
    with viz_col:
        fig = px.pie(
            bike_types_df,
            values="count",
            names="bike type",
            title="Bike Types Visualization",
            color="bike type",
            color_discrete_map={
                "electric_bike": "#006400",
                "docked_bike": "#00FFFF",
                "classic_bike": "#0000FF",
            },
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

elif query_type == "Bike Types Used By Members":
    bike_types = queries.get_bikes_used_by_member()
    bike_types_list = list(bike_types)
    bike_types_df = pd.DataFrame(
        bike_types_list, columns=["count", "member_type", "bike_type"]
    )
    with data_col:
        st.caption("Bike Types Used By Members Data")
        st.dataframe(
            bike_types_df,
            use_container_width=True,
            hide_index=True,
            column_order=["member_type", "bike_type", "count"],
        )
    with viz_col:
        fig = px.bar(
            bike_types_df,
            x="bike_type",
            y="count",
            color="bike_type",
            labels={"count": "Number of Rides", "bike_type": "Bike Type"},
            title="Number of Rides per Bike Type for Members",
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

elif query_type == "Average trip duration per user types":
    user_average_duration = queries.get_average_trip_duration_by_user_type()
    user_average_duration_list = list(user_average_duration)
    user_average_duration_df = pd.DataFrame(
        user_average_duration_list, columns=["member_type", "average_duration"]
    )
    user_average_duration_df["average_duration"] = (
        user_average_duration_df["average_duration"] / 60000
    )
    with data_col:
        st.caption("Average trip duration per user types")
        st.dataframe(
            user_average_duration_df,
            use_container_width=True,
            hide_index=True,
            column_order=["member_type", "average_duration"],
        )
    with viz_col:
        fig = px.bar(
            user_average_duration_df,
            x="member_type",
            y="average_duration",
            color="member_type",
            labels={
                "member_type": "Member Type",
                "average_duration": "Average Duration (in minutes)",
            },
            title="Average trip duration per user types",
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

elif query_type == "Popular Stations":
    popular_stations_cursor = queries.most_popular_stations()
    popular_stations_list = list(popular_stations_cursor)
    popular_stations_data = popular_stations_list[0]
    popular_start_df = pd.DataFrame(
        popular_stations_data["popular_start_stations"],
        columns=["count", "start station name"],
    )
    popular_end_df = pd.DataFrame(
        popular_stations_data["popular_end_stations"],
        columns=["count", "end station name"],
    )

    with data_col:
        st.caption("Popular Start Stations")
        st.dataframe(
            popular_start_df,
            hide_index=True,
            use_container_width=True,
            column_order=["start station name", "count"],
        )

        st.caption("Popular End Stations")
        st.dataframe(
            popular_end_df,
            hide_index=True,
            use_container_width=True,
            column_order=["end station name", "count"],
        )

    with viz_col:
        fig_start = px.bar(
            popular_start_df,
            x="start station name",
            y="count",
            title="Most Popular Start Stations",
            labels={"count": "Ride Count", "start station name": "Station Name"},
        )
        st.plotly_chart(fig_start, use_container_width=True)

        # Plot for popular end stations
        fig_end = px.bar(
            popular_end_df,
            x="end station name",
            y="count",
            title="Most Popular End Stations",
            labels={"count": "Ride Count", "end station name": "Station Name"},
        )
        st.plotly_chart(fig_end, use_container_width=True)

elif query_type == "Peak Hours":
    peak_hours_cursor = queries.get_peak_usage_hours()
    peak_hours_list = list(peak_hours_cursor)
    peak_hours_df = pd.DataFrame(peak_hours_list, columns=["hour", "count"])
    peak_hours_df = peak_hours_df.sort_values(by="hour")
    peak_hours_df.rename(columns={"count": "trip_count"}, inplace=True)

    with data_col:
        st.caption("Peak Hours Data")
        st.dataframe(
            peak_hours_df,
            hide_index=True,
            use_container_width=True,
            column_order=["hour", "trip_count"],
        )

    with viz_col:
        st.line_chart(peak_hours_df, x="hour", y="trip_count", use_container_width=True)

elif query_type == "Peak Hours With Day":
    peak_hours_cursor = queries.get_peak_usage_hours_with_day()
    peak_hours_list = list(peak_hours_cursor)
    peak_hours_df = pd.DataFrame(peak_hours_list, columns=["hour", "day", "count"])
    peak_hours_df["hour_group"] = peak_hours_df["hour"].apply(
        lambda x: f"{x}:00 - {x + 1}:00"
    )

    peak_hours_df["day"] = peak_hours_df["day"].replace(
        {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday",
            7: "Sunday",
        }
    )
    peak_hours_df["day"] = pd.Categorical(
        peak_hours_df["day"],
        categories=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        ordered=True,
    )
    peak_hours_df = peak_hours_df.sort_values(
        by=["day", "hour"], ascending=[True, True]
    )
    peak_hours_df.rename(columns={"count": "trip_count"}, inplace=True)

    with data_col:
        st.caption("Peak Hours Data With Day")
        st.dataframe(
            peak_hours_df,
            hide_index=True,
            use_container_width=True,
            column_order=["hour_group", "day", "trip_count"],
        )

    with viz_col:
        peak_hours_df = peak_hours_df.sort_values(
            by=["day", "hour"], ascending=[False, True]
        )
        fig = px.density_heatmap(
            peak_hours_df,
            x="hour",
            y="day",
            z="trip_count",
            labels={"hour": "Hour", "trip_count": "Trip Count", "day": "Day"},
            title="Peak Hours With Day Heatmap",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True)

