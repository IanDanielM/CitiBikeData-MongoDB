from etl.extract import ExtractTransformLoad


class Queries(ExtractTransformLoad):
    def __init__(self, db_name: str, collection_name: str):
        super().__init__(db_name, collection_name)

    # all data
    def get_data(self, page_num=1, page_size=50) -> list:
        skip = (page_num - 1) * page_size
        return self.default_collection.find({}, {"_id": 0,
                                                 "start station name": 1,
                                                 "end station name": 1,
                                                 "tripduration": 1,
                                                 "bikeid": 1,
                                                 "usertype": 1}).skip(skip).limit(page_size)

    # total trips
    def get_total_trips(self) -> int:
        return self.default_collection.count_documents({})

    # specific record
    def find_bike(self, value: int):
        return self.default_collection.find_one({"bikeid": value})

    def get_unique_start_stations(self):
        return self.default_collection.distinct("start station name")

    # Average Trip Duration
    def get_average_trip_duration(self):
        return self.default_collection.aggregate(
            [
                {
                    "$addFields": {
                        "converted_starttime": {"$toDate": "$starttime"},
                        "converted_stoptime": {"$toDate": "$stoptime"}
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
                        "converted_starttime": {"$toDate": "$starttime"},
                        "converted_stoptime": {"$toDate": "$stoptime"}
                    }
                },
                {
                    "$group": {
                        "_id": "$bikeid",
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
        return self.default_collection.find({'usertype': 'Subscriber'},
                                            {'usertype': 1,
                                             'gender': 1,
                                             'tripduration': 1,
                                             '_id': 0})

    # Count by Gender: Count the number of records for each 'gender'.
    def gender_count(self):
        return self.default_collection.aggregate(
            [
                {
                    "$group": {
                        "_id": "$gender",
                        "count": {"$sum": 1}
                    }
                }
            ]

        )

    # Birth Year Range: Find all trips made by users born between 1980 and 1990.
    def birth_year_range(self):
        return self.default_collection.find({
            "birth year": {"$lt": 1990, "$gte": 1980}},
            {'usertype': 1, 'gender': 1, 'tripduration': 1, 'birth year': 1, '_id': 0})

    # Group by Start Station: Count the number of trips that started from each 'start station name'.
    def group_by_start_station(self):
        return self.default_collection.aggregate(
            [
                {
                    "$group": {
                        "_id": "$start station name",
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
                        "converted_starttime": {"$toDate": "$starttime"},
                        "converted_stoptime": {"$toDate": "$stoptime"}
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
                        "bikeid": 1,
                        "duration": 1,
                        "start station name": 1,
                        "end station name": 1,
                        "_id": 0
                    }
                }
            ]
        )

    # Start and Stop Station Same: Find records where the start and end stations are the same.
    def find_same_start_end_stations(self):
        return self.default_collection.find({"$expr": {"$eq": [
            "$start station name",
            "$end station name"]}},
            {
            "_id": 0,
            "start station name": 1,
            "end station name": 1,
            "tripduration": 1
        })

    # Bikes Used Most Frequently: List the top 5 most frequently used 'bikeid'.
    def most_used_bikes(self):
        return self.default_collection.aggregate([
            {
                "$group": {
                    "_id": "$bikeid",
                    "usage_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"usage_count": -1}
            },
            {
                "$limit": 5
            }
        ])

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
                    "converted_starttime": {"$toDate": "$starttime"}
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
                        "converted_starttime": {"$toDate": "$starttime"},
                        "converted_stoptime": {"$toDate": "$stoptime"}
                    }
                },
                {
                    "$group": {
                        "_id": "$usertype",
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
                    {"$group": {"_id": "$start station name", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 5}
                ],
                "popular_end_stations": [
                    {"$group": {"_id": "$end station name", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 5}
                ]
            }
            }
        ])

    # Aggregate by Birth Year and Gender: Aggregate the data by 'birth year' and 'gender', counting trips for each group.
    def aggregate_by_birth_year_and_gender(self):
        return self.default_collection.aggregate([
            {
                "$group": {
                    "_id": {
                        "birth_year": "$birth year",
                        "gender": "$gender"
                    },
                    "tripCount": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.birth_year": 1, "_id.gender": 1}
            }
        ])
