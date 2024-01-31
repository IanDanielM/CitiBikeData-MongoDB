import datetime as dt
from datetime import datetime

import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static

from app.etl.extract import ExtractTransformLoad


class CustomQuery(ExtractTransformLoad):
    def __init__(self, db_name: str, collection_name: str, **kwargs) -> None:
        super().__init__(db_name, collection_name, **kwargs)

    def sidebar_filter(self):
        """
        Displays a sidebar with filter options for custom query building.

        Returns:
            tuple: A tuple containing the selected start date, end date,
            start station, end station, ride type, and user type.
        """
        st.sidebar.title("Custom Query Builder")
        default_start_date = dt.datetime(2023, 1, 1)
        default_end_date = dt.datetime(2023, 1, 31)
        start_date = st.sidebar.date_input("Start Date", default_start_date)
        end_date = st.sidebar.date_input("End Date", default_end_date)
        start_station = st.sidebar.selectbox(
            "Start Station",
            ["All"] + [
                station
                for station in self.default_collection.distinct("start_station_name")
            ],
        )
        end_station = st.sidebar.selectbox(
            "End Station",
            ["All"] + [
                station
                for station in self.default_collection.distinct("end_station_name")
            ],
        )
        ride_type = st.sidebar.selectbox(
            "Select Ride Type",
            ["All"] + [ride for ride in self.default_collection.distinct("rideable_type")],
        )
        user_type = st.sidebar.selectbox(
            "Select User Type",
            ["All"] + [user for user in self.default_collection.distinct("member_casual")],
        )

        return start_date, end_date, start_station, end_station, ride_type, user_type

    def custom_query(self) -> dict:
        """
        Constructs a query based on the provided filter parameters.

        Returns:
            A dictionary representing the MongoDB query.
        """
        (
            start_date,
            end_date,
            start_station,
            end_station,
            ride_type,
            user_type,
        ) = self.sidebar_filter()
        query = {}
        if start_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            query["started_at"] = {"$gte": start_datetime}
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query["ended_at"] = {"$lte": end_datetime}
        if start_station != "All":
            query["start_station_name"] = start_station
        if end_station != "All":
            query["end_station_name"] = end_station
        if ride_type != "All":
            query["rideable_type"] = ride_type
        if user_type != "All":
            query["member_casual"] = user_type

        return query

    def get_custom_query(self, query: dict) -> pd.DataFrame:
        """
        Retrieves custom data from the default collection based on the provided query.

        Args:
            query (dict): The query to filter the data.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the retrieved custom data.
        """
        custom_data = self.default_collection.find(
            query,
            {
                "_id": 0,
                "started_at": 1,
                "ended_at": 1,
                "start_station_name": 1,
                "end_station_name": 1,
                "rideable_type": 1,
                "member_casual": 1,
            },
        )
        custom_data_list = list(custom_data)
        custom_data_df = pd.DataFrame(custom_data_list)

        return custom_data_df

    def custom_visualize_data(self, custom_data_df: pd.DataFrame, data_col, viz_col) -> None:
        """
        Visualizes custom data using various plots based on the columns present in the DataFrame.

        Args:
            custom_data_df (pd.DataFrame): The DataFrame containing the custom data to be visualized.
            data_col: The column where the data will be displayed.
            viz_col: The column where the visualizations will be displayed.

        Returns:
            None
        """
        if custom_data_df.empty:
            st.error("No data to be Visualized")
            return
        with data_col:
            st.caption("Custom Query Results")
            st.dataframe(custom_data_df, hide_index=True, use_container_width=True)

        with viz_col:
            if custom_data_df.empty:
                st.error("No data to be Visualized")

            if "started_at" in custom_data_df.columns:
                custom_data_df["date"] = custom_data_df["started_at"].dt.date
                daily_counts = (
                    custom_data_df.groupby("date").size().reset_index(name="count")
                )
                fig = px.line(
                    daily_counts, x="date", y="count", title="Number of Rides Over Time"
                )
                st.plotly_chart(fig)

            if "rideable_type" in custom_data_df.columns:
                # dont visualize when rideable_type is selected
                if custom_data_df["rideable_type"].nunique() == 1:
                    pass
                else:
                    fig = px.pie(
                        custom_data_df,
                        names="rideable_type",
                        title="Distribution of Bike Types",
                    )
                    st.plotly_chart(fig)

            if "member_casual" in custom_data_df.columns:
                # dont visualize when member_casual is selected
                if custom_data_df["member_casual"].nunique() == 1:
                    pass
                else:
                    fig = px.pie(
                        custom_data_df,
                        names="member_casual",
                        title="Distribution of User Types",
                    )
                    st.plotly_chart(fig)

    def get_map_query(self, query: dict) -> pd.DataFrame:
        """
        Retrieves map data based on the provided query.

        Args:
            query (dict): The query to filter the map data.

        Returns:
            pd.DataFrame: A DataFrame containing the map data.
        """
        map_data = self.default_collection.aggregate(
            [
                {"$match": query},
                {"$sample": {"size": 1000}},
                {
                    "$project": {
                        "_id": 0,
                        "start_station_name": 1,
                        "end_station_name": 1,
                        "start_lat": 1,
                        "start_lng": 1,
                        "end_lat": 1,
                        "end_lng": 1,
                        "started_at": 1,
                        "ended_at": 1,
                        "rideable_type": 1,
                        "member_casual": 1,
                    }
                },
            ]
        )
        map_data_list = list(map_data)
        map_data_df = pd.DataFrame(map_data_list)

        return map_data_df

    def map_visualize_data(self, map_data_df: pd.DataFrame) -> None:
        """
        Visualizes trip data on a map.

        Args:
            map_data_df (pd.DataFrame): DataFrame containing trip data.

        Returns:
            None
        """
        try:
            st.caption("Map Visualization")

            if map_data_df.empty:
                st.write("No trips found for the selected filters.")
                return

            try:
                avg_lat = map_data_df["start_lat"].mean()
                avg_lng = map_data_df["start_lng"].mean()
            except (KeyError, TypeError, ValueError):
                st.error("An error occurred while visualizing the map.")
                return
            trip_map = folium.Map(location=[avg_lat, avg_lng], zoom_start=15)

            # Prepare data for markers and lines
            start_coords = map_data_df[["start_lat", "start_lng"]].values.tolist()
            end_coords = map_data_df[["end_lat", "end_lng"]].values.tolist()
            start_station_names = map_data_df["start_station_name"].values.tolist()
            end_station_names = map_data_df["end_station_name"].values.tolist()

            # Add markers and lines to the map
            for start, end, start_name, end_name in zip(start_coords, end_coords, start_station_names, end_station_names):
                folium.Marker(
                    start,
                    tooltip=start_name,
                    icon=folium.Icon(color="green", icon="play"),
                    popup=f"Trip Starts at [{start_name} ends at {end_name}]",
                ).add_to(trip_map)
                folium.Marker(
                    end,
                    tooltip=end_name,
                    icon=folium.Icon(color="red", icon="stop"),
                    popup=f"Trip Starts at [{start_name} ends at {end_name}]",
                ).add_to(trip_map)
                folium.PolyLine(
                    [start, end], color="gray", weight=1.5, opacity=1
                ).add_to(trip_map)
            folium_static(trip_map, width=1000)
        except Exception as error:
            st.error("An error occurred while visualizing the map.", error)
