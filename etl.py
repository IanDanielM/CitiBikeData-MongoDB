from app.etl.extract import ExtractTransformLoad


def main():
    etl = ExtractTransformLoad("citibike", "trips")
