from app.etl.extract import ExtractTransformLoad


def main():
    etl = ExtractTransformLoad("citibike", "trips")
    base_url = ""
    etl.ingest_data(base_url, 2023, "app/etl/data", "trips")


if __name__ == "__main__":
    main()
