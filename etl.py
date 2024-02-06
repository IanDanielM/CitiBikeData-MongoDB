import os
import argparse
import streamlit as st
from app.etl.extract import ExtractTransformLoad


def main(
    db: str, collection: str, uri: str, base_url: str, year: int, file_path: str
) -> None:
    """
    Main function for performing the ETL process.

    Args:
        db (str): The name of the database.
        collection (str): The name of the collection.
        uri (str): The URI for connecting to the MongoDB server.
        base_url (str): The base URL for data ingestion.
        year (int): The year for filtering the data.
        file_path (str): The file path for the data file.

    Returns:
        None
    """
    etl = ExtractTransformLoad(db, collection, uri)
    etl.ingest_data(base_url, year, file_path, collection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ETL process")
    parser.add_argument("--db", type=str, required=True, help="Database name")
    parser.add_argument("--collection", type=str, required=True, help="Collection name")
    parser.add_argument("--uri", type=str, required=True, help="MongoDB URI")
    parser.add_argument(
        "--base_url", type=str, required=True, help="Base URL for data ingestion"
    )
    parser.add_argument(
        "--year", type=int, required=True, help="Year for data filtering"
    )
    parser.add_argument(
        "--file_path", type=str, required=True, help="File path for data file"
    )

    args = parser.parse_args()

    main(
        db=args.db,
        collection=args.collection,
        uri=args.uri,
        base_url=args.base_url,
        year=args.year,
        file_path=args.file_path,
    )
