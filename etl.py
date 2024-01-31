from app.etl.extract import ExtractTransformLoad


def main():
    uri = "mongodb+srv://iandan874:iamiandaniel@cluster0.wb90azp.mongodb.net/?retryWrites=true&w=majority"
    etl = ExtractTransformLoad("citibike", "trips", uri=uri)
    base_url = "https://s3.amazonaws.com/tripdata/JC-202301-citibike-tripdata.csv.zip"
    etl.ingest_data(base_url, 2023, "app/etl/data", "trips")


if __name__ == "__main__":
    main()
