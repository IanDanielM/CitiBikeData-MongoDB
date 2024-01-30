import streamlit as st
from app.etl.extract import ExtractTransformLoad
from datetime import datetime
import pandas as pd
import plotly.express as px
import pymongo


class CustomQuery(ExtractTransformLoad):
    def __init__(self, db_name: str, collection_name: str):
        super().__init__(db_name, collection_name)

    def sidebar_filter(self):
        st.sidebar.title("Custom Query Builder")
        start_date = st.sidebar.date_input("Start Date", datetime.now())
        end_date = st.sidebar.date_input("End Date", datetime.now())
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

    def custom_query(self):
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

    def get_custom_query(_self, query):
        custom_data = _self.default_collection.find(
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

    def custom_visualize_data(self, custom_data_df, data_col, viz_col):
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
                fig = px.pie(
                    custom_data_df,
                    names="member_casual",
                    title="Distribution of User Types",
                )
                st.plotly_chart(fig)
