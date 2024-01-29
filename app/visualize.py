import folium
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from etl.queries import Queries
from streamlit_folium import folium_static

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

# Get total trips and average trip duration
total_trips = queries.get_total_trips()
average_trip_duration = queries.get_average_trip_duration()
for duration in average_trip_duration:
    avg_duration = round((duration["avg_duration"] / 60000), 2)


def lat_lon_to_radians(df, lat_col, lon_col):
    return np.radians(df[[lat_col, lon_col]])


# Vectorized Haversine function
def haversine_vectorized(start_lats, start_lons, end_lats, end_lons):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    start_lats, start_lons, end_lats, end_lons = map(
        np.radians, [start_lats, start_lons, end_lats, end_lons]
    )

    # Differences in coordinates
    dlat = end_lats - start_lats
    dlon = end_lons - start_lons

    # Haversine formula
    a = (
        np.sin(dlat / 2.0) ** 2
        + np.cos(start_lats) * np.cos(end_lats) * np.sin(dlon / 2.0) ** 2
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance


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
            "Peak Hours",
            "Peak Hours With Day",
            "Total Trips Per Month",
            "Average trip duration per user types",
            "Average Speed Per User Type",
            "Visualize Trip Data",
        ],
    )

data_col, viz_col = st.columns(2)

if query_type == "User Types":
    user_types = queries.count_by_user_type()
    user_types_list = list(user_types)
    user_types_df = pd.DataFrame(user_types_list, columns=["count", "usertype"])

    with data_col:
        # Data for user types
        st.caption("User Types Data")
        st.dataframe(user_types_df, use_container_width=True, hide_index=True)

    with viz_col:
        # Plot for user types
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
        # Data for bike types
        st.caption("Bike Types Data")
        st.dataframe(
            bike_types_df,
            use_container_width=True,
            hide_index=True,
            column_order=["bike type", "count"],
        )
    with viz_col:
        # Plot for bike types
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
        # Data for bike types used by members
        st.caption("Bike Types Used By Members Data")
        st.dataframe(
            bike_types_df,
            use_container_width=True,
            hide_index=True,
            column_order=["member_type", "bike_type", "count"],
        )
    with viz_col:
        # Plot for bike types used by members
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
    # calculate average duration in minutes
    user_average_duration_df["average_duration"] = (
        user_average_duration_df["average_duration"] / 60000
    )
    with data_col:
        # Data for average trip duration per user types
        st.caption("Average trip duration per user types")
        st.dataframe(
            user_average_duration_df,
            use_container_width=True,
            hide_index=True,
            column_order=["member_type", "average_duration"],
        )
    with viz_col:
        # Plot for average trip duration per user types
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
        # Data for popular stations
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
        # Plot for popular start stations
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
        # Data for peak hours
        st.caption("Peak Hours Data")
        st.dataframe(
            peak_hours_df,
            hide_index=True,
            use_container_width=True,
            column_order=["hour", "trip_count"],
        )

    with viz_col:
        # Plot for peak hours
        fig = px.line(
            peak_hours_df,
            x="hour",
            y="trip_count",
            title="Peak Hours Visualization",
            labels={"hour": "Hour", "trip_count": "Trip Count"},
        )
        st.plotly_chart(fig, use_container_width=True)

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
        # Data for peak hours with day
        st.caption("Peak Hours Data With Day")
        st.dataframe(
            peak_hours_df,
            hide_index=True,
            use_container_width=True,
            column_order=["hour_group", "day", "trip_count"],
        )

    with viz_col:
        # Plot for peak hours with day
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

elif query_type == "Average Speed Per User Type":
    average_speed_cursor = queries.get_raw_trip_data()
    average_speed_list = list(average_speed_cursor)
    average_speed_df = pd.DataFrame(average_speed_list)
    average_speed_df["distance"] = haversine_vectorized(
        average_speed_df["start_lat"],
        average_speed_df["start_lng"],
        average_speed_df["end_lat"],
        average_speed_df["end_lng"],
    )

    # Calculate duration in hours
    average_speed_df["duration_hours"] = (
        average_speed_df["ended_at"] - average_speed_df["started_at"]
    ).dt.total_seconds() / 3600

    # Calculate speed
    average_speed_df = average_speed_df[average_speed_df["duration_hours"] > 0]
    average_speed_df["speed"] = (
        average_speed_df["distance"] / average_speed_df["duration_hours"]
    )

    # Group by 'member_casual' and calculate average speed
    average_speed_per_user_type = average_speed_df.groupby("member_casual")[
        "speed"
    ].mean()
    average_speed_per_user_type = average_speed_per_user_type.reset_index()
    average_speed_per_user_type["speed"] = average_speed_per_user_type["speed"].round(2)
    average_speed_per_user_type.rename(
        columns={"member_casual": "Member Type", "speed": "Average Speed (km/h)"},
        inplace=True,
    )

    # Group by bike type and calculate average speed
    average_speed_per_bike_type = average_speed_df.groupby("rideable_type")[
        "speed"
    ].mean()
    average_speed_per_bike_type = average_speed_per_bike_type.reset_index()
    average_speed_per_bike_type["speed"] = average_speed_per_bike_type["speed"].round(2)
    average_speed_per_bike_type.rename(
        columns={"rideable_type": "Bike Type", "speed": "Average Speed (km/h)"},
        inplace=True,
    )

    with data_col:
        st.caption("Average Speed Per User Type")
        st.dataframe(
            average_speed_per_user_type,
            hide_index=True,
            use_container_width=True,
            column_order=["Member Type", "Average Speed (km/h)"],
        )

        st.caption("Average Speed Per Bike Type")
        st.dataframe(
            average_speed_per_bike_type,
            hide_index=True,
            use_container_width=True,
            column_order=["Bike Type", "Average Speed (km/h)"],
        )

    with viz_col:
        # Plot for average speed per user type
        fig = px.bar(
            average_speed_per_user_type,
            x="Member Type",
            y="Average Speed (km/h)",
            color="Member Type",
            labels={
                "Member Type": "Member Type",
                "Average Speed (km/h)": "Average Speed (km/h)",
            },
            title="Average Speed Per User Type",
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

        # Plot for average speed per bike type
        fig = px.bar(
            average_speed_per_bike_type,
            x="Bike Type",
            y="Average Speed (km/h)",
            color="Bike Type",
            labels={
                "Bike Type": "Bike Type",
                "Average Speed (km/h)": "Average Speed (km/h)",
            },
            title="Average Speed Per Bike Type",
        )
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")


elif query_type == "Visualize Trip Data":
    trip_data_cursor = queries.get_trip_data()
    trip_data_list = list(trip_data_cursor)
    trip_data_df = pd.DataFrame(trip_data_list)
    trip_data_df.dropna(inplace=True)
    avg_lat = trip_data_df["start_lat"].mean()
    avg_lng = trip_data_df["start_lng"].mean()

    # Create a map object
    trip_map = folium.Map(location=[avg_lat, avg_lng], zoom_start=15)
    for _, row in trip_data_df.iterrows():
        start_coords = [row["start_lat"], row["start_lng"]]
        end_coords = [row["end_lat"], row["end_lng"]]

        folium.Marker(
            start_coords,
            tooltip=row["start_station_name"],
            icon=folium.Icon(color="green", icon="play"),
            popup=f"Trip Starts at [{row['start_station_name']} ends at {row['end_station_name']}]",
        ).add_to(trip_map)

        folium.Marker(
            end_coords,
            tooltip=row["end_station_name"],
            icon=folium.Icon(color="red", icon="stop"),
            popup=f"Trip Starts at [{row['start_station_name']} ends at {row['end_station_name']}]",
        ).add_to(trip_map)
        folium.PolyLine(
            [start_coords, end_coords], color="gray", weight=1.5, opacity=1
        ).add_to(trip_map)

    # Display the map
    folium_static(trip_map, width=1000)
