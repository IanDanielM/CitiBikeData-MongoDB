import pandas as pd
import plotly.express as px
import streamlit as st

from app.visualize.helpers import haversine_vectorized
from app.etl.queries import Queries


def st_user_types(queries: Queries, data_col, viz_col):
    """
    Visualizes user types data and plots a pie chart.

    Args:
        queries (Queries): Queries containing methods to query user types data.
        data_col: Streamlit column to display the user types data.
        viz_col: Streamlit column to display the pie chart visualization.

    Returns:
        None
    """
    try:
        user_types_cursor = queries.count_by_user_type()
        user_types_list = list(user_types_cursor)
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def st_bike_types(queries: Queries, data_col, viz_col) -> None:
    """
    Visualizes bike types data and plots a pie chart.

    Parameters:
    - queries: An object containing methods to query bike data.
    - data_col: The column to display the data in the UI.
    - viz_col: The column to display the visualization in the UI.

    Returns:
    None
    """
    try:
        bike_types_cursor = queries.bike_count()
        bike_types_list = list(bike_types_cursor)
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def st_bike_types_used_by_members(queries: Queries, data_col, viz_col) -> None:
    """
    Visualizes the bike types used by members.

    Args:
        queries (Queries): An object containing query methods.
        data_col: The column to display the data in.
        viz_col: The column to display the visualization in.
    """
    try:
        bike_types_cursor = queries.get_bikes_used_by_member()
        bike_types_list = list(bike_types_cursor)
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def st_average_trip_duration_per_user_types(queries: Queries, data_col, viz_col) -> None:
    """
    Visualizes the average trip duration per user types.

    Args:
        queries (Queries): An object containing query methods.
        data_col: The column to display the data in.
        viz_col: The column to display the visualization in.
    """
    try:
        user_average_duration_cursor = queries.get_average_trip_duration_by_user_type()
        user_average_duration_list = list(user_average_duration_cursor)
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def st_popular_stations(queries: Queries, data_col, viz_col) -> None:
    """
    Visualizes the most popular start and end stations using Streamlit.

    Args:
        queries: An object that provides access to the database queries.
        data_col: The Streamlit column to display the dataframes.
        viz_col: The Streamlit column to display the plots.

    Returns:
        None
    """
    try:
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def st_peak_hours(queries, data_col, viz_col) -> None:
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


def st_peak_hours_with_day(queries: Queries, data_col, viz_col) -> None:
    """
    Visualizes peak usage hours with day.

    Args:
        queries: An object that provides methods to retrieve peak usage hours data.
        data_col: The streamlit column to display the data.
        viz_col: The streamlit column to display the visualization.

    Returns:
        None
    """
    try:
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def st_total_trips_per_month(queries, data_col_id, viz_col_id) -> None:
    """
    Visualizes the total number of trips per month.

    Args:
        queries: An object containing the queries to retrieve the total trips per month.
        data_col_id: The ID of the column to display the data.
        viz_col_id: The ID of the column to display the plot.

    Returns:
        None
    """
    try:
        total_trips_cursor = queries.get_total_trips_per_month()
        total_trips_list = list(total_trips_cursor)
        total_trips_df = pd.DataFrame(total_trips_list, columns=["month", "total_trips"])
        total_trips_df["month"] = total_trips_df["month"].replace(
            {
                1: "January",
                2: "February",
                3: "March",
                4: "April",
                5: "May",
                6: "June",
                7: "July",
                8: "August",
                9: "September",
                10: "October",
                11: "November",
                12: "December",
            }
        )

        with data_col_id:
            # Data for total trips per month
            st.caption("Total Trips Per Month Data")
            st.dataframe(
                total_trips_df,
                hide_index=True,
                use_container_width=True,
                column_order=["month", "total_trips"],
            )

        with viz_col_id:
            # Plot for total trips per month
            fig = px.line(
                total_trips_df,
                x="month",
                y="total_trips",
                title="Total Trips Per Month",
                labels={"month": "Month", "total_trips": "Total Trips"},
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def st_average_speed_per_user_and_bike_type(queries: Queries, data_col, viz_col) -> None:
    """
    Calculate and visualize the average speed per user type and bike type.

    Args:
        queries (Queries): Object containing query methods.
        data_col: Streamlit column for displaying data.
        viz_col: Streamlit column for displaying visualizations.
    """
    try:
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
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return
