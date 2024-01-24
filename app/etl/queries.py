from etl.extract import ExtractTransformLoad


class Queries(ExtractTransformLoad):
    def __init__(self, db_name: str, collection_name: str):
        super().__init__(db_name, collection_name)

    def count_documents(self) -> int:
        return self.default_collection.count_documents({})

    # all data
    def get_data(self, page_num=1, page_size=51) -> list:
        skip = (page_num - 1) * page_size
        return self.default_collection.find({}, {"_id": 0,
                                                 "start_station_name": 1,
                                                 "end_station_name": 1,
                                                 "rideable_type": 1,
                                                 "member_casual": 1}).skip(skip).limit(page_size)

    # total trips
    def get_total_trips(self) -> int:
        return self.default_collection.count_documents({})

    # specific record
    def bike_count(self, value: int):
        return self.default_collection.aggregate(
            [
                {
                    "$group": {
                        "_id": "$rideable_type",
                        "count": {"$sum": 1}
                    }
                }
            ]
        )

    def get_unique_start_stations(self):
        return self.default_collection.distinct("start station name")

    # Average Trip Duration
    def get_average_trip_duration(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$started_at"},
                        "converted_stoptime": {"$toDate": "$ended_at"}
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "avg_duration": {
                            "$avg": {
                                "$subtract": ["$converted_stoptime",
                                              "$converted_starttime"]
                            }
                        }
                    }
                }
            ]
        )

    # Average Trip Duration by Bike ID
    def get_average_trip_duration_by_bike(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$started_at"},
                        "converted_stoptime": {"$toDate": "$ended_at"}
                    }
                },
                {
                    "$group": {
                        "_id": "$rideable_type",
                        "avg_duration": {
                            "$avg": {
                                "$subtract": ["$converted_stoptime",
                                              "$converted_starttime"]
                            }
                        }
                    }
                }
            ]
        )

    # Sort Records by Trip Duration
    def sort_by_trip_duration(self):
        return self.default_collection.find({}, {'bikeid': 1,
                                                 'tripduration': 1,
                                                 '_id': 0}
                                            ).sort("tripduration", -1)

    # Filter by User Type: Find all records where 'usertype' is 'Subscriber'.
    def filter_by_user_type(self):
        return self.default_collection.find({'member_casual': 'member'},
                                            {'member_casual': 1,
                                             'rideable_type': 1,
                                             '_id': 0})

    # Count by User Type: Count the number of records for each 'usertype'.
    def count_by_user_type(self):
        return self.default_collection.aggregate(
            [
                {
                    "$group": {
                        "_id": "$member_casual",
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "usertype": "$_id",
                        "_id": 0,
                        "count": 1
                    }
                }
            ]
        )

    # Group by Start Station: Count the number of trips that started from each 'start station name'.
    def group_by_start_station(self):
        return self.default_collection.aggregate(
            [
                {
                    "$group": {
                        "_id": "$start_station_name",
                        "count": {
                            "$sum": 1
                        }
                    }
                }
            ]
        )

    # Longest Trips: Find the 10 longest trips in terms of 'tripduration'.
    def longest_trips(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$started_at"},
                        "converted_stoptime": {"$toDate": "$ended_at"}
                    }
                },
                {
                    "$addFields": {
                        "duration": {
                            "$subtract": ["$converted_stoptime",
                                          "$converted_starttime"]
                        }
                    }
                },
                {
                    "$sort": {"duration": -1}
                },
                {
                    "$limit": 10
                },
                {
                    "$project": {
                        "rideable_type": 1,
                        "duration": 1,
                        "start_station_name": 1,
                        "end_station_name": 1,
                        "_id": 0
                    }
                }
            ]
        )

    # Start and Stop Station Same: Find records where the start and end stations are the same.
    def find_same_start_end_stations(self):
        return self.default_collection.find({"$expr": {"$eq": [
            "$start_station_name",
            "$end_station_name"]}},
            {
            "_id": 0,
            "start_station_name": 1,
            "end_station_name": 1,
        })

    # Calculate Distance Traveled: Calculate the approximate distance traveled for each trip (using 'start station latitude/longitude' and 'end station latitude/longitude').
    def distane_covered_by_coordinates(self):
        return self.default_collection.aggregate([
            {
                "$addFields": {
                    "latitude": {
                        "$subtract": ["$start station latitude",
                                      "$end station latitude"]
                    }
                }
            },
            {
                "$addFields": {
                    "longitude": {
                        "$subtract": ["$start station longitude",
                                      "$end station longitude"]
                    }
                }
            },
            {
                "$project": {
                    "tripduration": 1,
                    "latitude": 1,
                    "longitude": 1,
                    "_id": 0
                }
            }
        ])

    # Month-wise Trip Count: Count the number of trips made in each month.
    def total_trips_per_month(self):
        return self.default_collection.aggregate([
            {
                "$addFields": {
                    "converted_starttime": {"$toDate": "$started_at"}
                }
            },
            {
                "$addFields": {
                    "month": {"$month": "$converted_starttime"}
                }
            },
            {
                "$group": {
                    "_id": "$month",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ])

    # Find Trips on Specific Date: Find all trips started on '2013-06-01'.
    def get_trips_on_specific_date(self, date):
        return self.default_collection.aggregate([
            {
                "$addFields": {
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": {"$toDate": "$starttime"}
                        }
                    }
                }
            },
            {
                "$match": {
                    "date": date
                }
            },
            {
                "$project": {
                    "bikeid": 1,
                    "tripduration": 1,
                    "start station name": 1,
                    "end station name": 1,
                    "_id": 0
                }
            }
        ])

    # Average Trip Duration by User Type: Calculate the average trip duration for each 'usertype'.
    def get_average_trip_duration_by_user_type(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$started_at"},
                        "converted_stoptime": {"$toDate": "$ended_at"}
                    }
                },
                {
                    "$group": {
                        "_id": "$member_casual",
                        "avg_duration": {
                            "$avg": {
                                "$subtract": ["$converted_stoptime",
                                              "$converted_starttime"]
                            }
                        }
                    }
                }
            ]
        )

    # Most Popular Stations: Find the most popular start and end stations.
    def most_popular_stations(self):
        return self.default_collection.aggregate([
            {"$facet": {
                "popular_start_stations": [
                    {"$group": {"_id": "$start_station_name", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 5}
                ],
                "popular_end_stations": [
                    {"$group": {"_id": "$end_station_name", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 5}
                ]
            }
            }
        ])
