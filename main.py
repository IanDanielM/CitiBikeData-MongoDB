from etl.extract import ExtractTransformLoad
from etl.queries import Queries

# etl
etl = ExtractTransformLoad("citibike", "trips")
data = etl.extract_data("etl/files/201306-citibike-tripdata.csv")
etl.load_data(data)

# queries
queries = Queries("citibike", "trips")
data = queries.aggregate_by_birth_year_and_gender()
for data in data:
    print(data)
