from app.etl.extract import ExtractTransformLoad
import streamlit as st


class Queries(ExtractTransformLoad):
    def __init__(self, db_name: str, collection_name: str):
        super().__init__(db_name, collection_name)

    # count total documents
    @st.cache_data(ttl=7200)
    def count_documents(self) -> int:
        return self.default_collection.count_documents({})

    # count total trips
    @st.cache_data(ttl=7200)
    def get_total_trips(self) -> int:
        return self.default_collection.count_documents({})

    # all data
    @st.cache_data(ttl=7200)
    def get_data(self, page_num=1, page_size=51) -> list:
        skip = (page_num - 1) * page_size
        return (
            self.default_collection.find(
                {},
                {
                    "_id": 0,
                    "start_station_name": 1,
                    "end_station_name": 1,
                    "rideable_type": 1,
                    "member_casual": 1,
                },
            )
            .skip(skip)
            .limit(page_size)
        )

    # get unique start stations
    @st.cache_data(ttl=7200)
    def get_unique_start_stations(self):
        return self.default_collection.distinct("start station name")

    # Get trip data without any transformations
    @st.cache_data(ttl=7200)
    def get_raw_trip_data(self):
        return self.default_collection.aggregate(
            [
                {
                    "$project": {
                        "_id": 0,
                        "member_casual": 1,
                        "rideable_type": 1,
                        "started_at": 1,
                        "ended_at": 1,
                        "start_lat": 1,
                        "start_lng": 1,
                        "end_lat": 1,
                        "end_lng": 1,
                    }
                }
            ]
        )

    # Get 1000 random trips
    @st.cache_data(ttl=7200)
    def get_trip_data(self):
        return self.default_collection.aggregate(
            [
                {"$sample": {"size": 1000}},
                {
                    "$project": {
                        "start_lat": 1,
                        "start_lng": 1,
                        "end_lat": 1,
                        "end_lng": 1,
                        "member_casual": 1,
                        "started_at": 1,
                        "ended_at": 1,
                        "start_station_name": 1,
                        "end_station_name": 1,
                    }
                },
            ]
        )

    # get bike type count
    @st.cache_data(ttl=7200)
    def bike_count(self):
        return self.default_collection.aggregate(
            [
                {"$group": {"_id": "$rideable_type", "count": {"$sum": 1}}},
                {"$project": {"bike type": "$_id", "_id": 0, "count": 1}},
            ]
        )

    # Average Trip Duration
    @st.cache_data(ttl=7200)
    def get_average_trip_duration(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$started_at"},
                        "converted_stoptime": {"$toDate": "$ended_at"},
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "avg_duration": {
                            "$avg": {
                                "$subtract": [
                                    "$converted_stoptime",
                                    "$converted_starttime",
                                ]
                            }
                        },
                    }
                },
            ]
        )

    # Average Trip Duration by Bike ID
    @st.cache_data(ttl=7200)
    def get_average_trip_duration_by_bike(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$started_at"},
                        "converted_stoptime": {"$toDate": "$ended_at"},
                    }
                },
                {
                    "$group": {
                        "_id": "$rideable_type",
                        "avg_duration": {
                            "$avg": {
                                "$subtract": [
                                    "$converted_stoptime",
                                    "$converted_starttime",
                                ]
                            }
                        },
                    }
                },
            ]
        )

    # Filter by User Type: Find all records where 'usertype' is 'Subscriber'.
    @st.cache_data(ttl=7200)
    def filter_by_user_type(self):
        return self.default_collection.find(
            {"member_casual": "member"},
            {"member_casual": 1, "rideable_type": 1, "_id": 0},
        )

    # Count by User Type: Count the number of records for each 'usertype'.
    @st.cache_data(ttl=7200)
    def count_by_user_type(self):
        return self.default_collection.aggregate(
            [
                {"$group": {"_id": "$member_casual", "count": {"$sum": 1}}},
                {"$project": {"usertype": "$_id", "_id": 0, "count": 1}},
            ]
        )

    # Group by Start Station: Count the number of trips that started from each 'start station name'.
    @st.cache_data(ttl=7200)
    def group_by_start_station(self):
        return self.default_collection.aggregate(
            [{"$group": {"_id": "$start_station_name", "count": {"$sum": 1}}}]
        )

    # Start and Stop Station Same: Find records where the start and end stations are the same.
    @st.cache_data(ttl=7200)
    def find_same_start_end_stations(self):
        return self.default_collection.find(
            {"$expr": {"$eq": ["$start_station_name", "$end_station_name"]}},
            {
                "_id": 0,
                "start_station_name": 1,
                "end_station_name": 1,
            },
        )

    # Month-wise Trip Count: Count the number of trips made in each month.
    @st.cache_data(ttl=7200)
    def get_total_trips_per_month(self):
        return self.default_collection.aggregate(
            [
                {"$addFields": {"converted_starttime": {"$toDate": "$started_at"}}},
                {"$addFields": {"month": {"$month": "$converted_starttime"}}},
                {"$group": {"_id": "$month", "total_trips": {"$sum": 1}}},
                {"$sort": {"_id": 1}},
                {"$project": {"month": "$_id", "total_trips": 1, "_id": 0}},
            ]
        )

    # Average Trip Duration by User Type
    @st.cache_data(ttl=7200)
    def get_average_trip_duration_by_user_type(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$started_at"},
                        "converted_stoptime": {"$toDate": "$ended_at"},
                    }
                },
                {
                    "$group": {
                        "_id": "$member_casual",
                        "average_duration": {
                            "$avg": {
                                "$subtract": [
                                    "$converted_stoptime",
                                    "$converted_starttime",
                                ]
                            }
                        },
                    }
                },
                {"$project": {"member_type": "$_id", "_id": 0, "average_duration": 1}},
            ]
        )

    # Most Popular Stations: Find the most popular start and end stations.
    @st.cache_data(ttl=7200)
    def most_popular_stations(self):
        return self.default_collection.aggregate(
            [
                {
                    "$facet": {
                        "popular_start_stations": [
                            {
                                "$group": {
                                    "_id": "$start_station_name",
                                    "count": {"$sum": 1},
                                }
                            },
                            {"$sort": {"count": -1}},
                            {"$limit": 10},
                            {
                                "$project": {
                                    "start station name": "$_id",
                                    "count": 1,
                                    "_id": 0,
                                }
                            },
                        ],
                        "popular_end_stations": [
                            {
                                "$group": {
                                    "_id": "$end_station_name",
                                    "count": {"$sum": 1},
                                }
                            },
                            {"$sort": {"count": -1}},
                            {"$limit": 10},
                            {
                                "$project": {
                                    "end station name": "$_id",
                                    "count": 1,
                                    "_id": 0,
                                }
                            },
                        ],
                    }
                }
            ]
        )

    # Get bikes used by members
    @st.cache_data(ttl=7200)
    def get_bikes_used_by_member(self):
        return self.default_collection.aggregate(
            [
                {"$match": {"member_casual": "member"}},
                {
                    "$group": {
                        "_id": "$rideable_type",
                        "count": {"$sum": 1},
                        "member_type": {"$first": "$member_casual"},
                    }
                },
                {"$sort": {"count": -1}},
                {
                    "$project": {
                        "bike_type": "$_id",
                        "count": 1,
                        "member_type": 1,
                        "_id": 0,
                    }
                },
            ]
        )

    # Peak Usage Hours
    @st.cache_data(ttl=7200)
    def get_peak_usage_hours(self):
        return self.default_collection.aggregate(
            [
                {"$addFields": {"hour": {"$hour": {"$toDate": "$started_at"}}}},
                {"$group": {"_id": "$hour", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$project": {"hour": "$_id", "count": 1, "_id": 0}},
            ]
        )

    # Peak Usage Hours by Day of Week
    @st.cache_data(ttl=7200)
    def get_peak_usage_hours_with_day(self):
        return self.default_collection.aggregate(
            [
                {
                    "$project": {
                        "hour_started": {"$hour": "$started_at"},
                        "day_of_week": {"$dayOfWeek": "$started_at"},
                    }
                },
                {
                    "$group": {
                        "_id": {"hour": "$hour_started", "dayOfWeek": "$day_of_week"},
                        "count": {"$sum": 1},
                    }
                },
                {"$sort": {"_id.hour": 1}},
                {
                    "$project": {
                        "hour": "$_id.hour",
                        "day": "$_id.dayOfWeek",
                        "count": 1,
                        "_id": 0,
                    }
                },
            ]
        )
