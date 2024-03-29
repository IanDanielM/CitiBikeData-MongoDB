import os
import zipfile

import pandas as pd
import streamlit as st
from pymongo import MongoClient
from typing import Optional


class ExtractTransformLoad:
    def __init__(
        self,
        db_name: str,
        collection_name: str = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        uri: Optional[str] = None,
    ) -> None:
        client: MongoClient
        if uri:
            client = MongoClient(uri)
        elif host and port:
            client = MongoClient(host, port)
        else:
            raise ValueError("Either `host` and `port` or `uri` must be provided.")

        self.client = client
        self.db = self.client[db_name]
        self.default_collection = None

        if collection_name:
            self.default_collection = self.get_collection(collection_name)

    def get_collection(self, collection_name: str = None) -> None:
        if collection_name:
            return self.db[collection_name]
        elif self.default_collection:
            return self.default_collection
        else:
            raise ValueError("No collection specified")

    @staticmethod
    def generate_monthly_urls(base_url: str, year: int) -> list:
        urls = []
        for month in range(1, 13):
            month_str = f"{year}{month:02d}"
            url = base_url.replace("202301", month_str)
            urls.append(url)
        return urls

    def extract_data(self, url: str, path: str) -> list:
        """
        Extracts data from a given URL and saves it to the specified path.
        Args:
            url (str): The URL of the data to be extracted.
            path (str): The path where the extracted data will be saved.
        Returns:
            str: The path of the extracted file if successful, None otherwise.
        """
        zip_name = os.path.join(path, url.split("/")[-1])
        os.system(f"wget {url} -O {zip_name}")
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith(".csv") and "__MACOSX" not in file:
                    zip_ref.extract(file, path)
                    return os.path.join(path, file)
        return None

    def process_data(self, csv_path: str, collection_name: str) -> list:
        """
        Transforms data from a CSV file

        Args:
            csv_path (str): The path to the CSV file.
            collection_name (str): The name of the MongoDB collection.

        Returns:
            list: The processed data as a list of dictionaries.

        Raises:
            Exception: If an error occurs while processing the data.
        """
        try:
            if csv_path:
                df = pd.read_csv(csv_path)
                df["started_at"] = pd.to_datetime(df["started_at"])
                df["ended_at"] = pd.to_datetime(df["ended_at"])
                df.dropna(inplace=True)
                data = df.to_dict("records")

                self.load_data(collection_name, data)
                os.remove(csv_path)
            else:
                print("No csv file found")
        except Exception as e:
            print(f"Error occurred while processing data: {e}")

    def load_data(self, collection_name: str, data: list) -> None:
        """
        Loads the given data into database.

        Args:
            collection_name (str): The name of the collection to load the data into.
            data (list): The list of data to be inserted into the collection.

        Returns:
            None
        """
        try:
            collection = self.get_collection(collection_name)
            collection.insert_many(data)
        except Exception as e:
            print(f"Error occurred while loading data: {e}")

    def ingest_data(
        self, base_url: str, year: int, path: str, collection_name: str
    ) -> None:
        """
        Perfoms the ETL process.

        Args:
            base_url (str): The base URL for the data.
            year (int): The year for which the data is to be ingested.
            path (str): The path where the downloaded zip files are stored.
            collection_name (str): The name of the collection in which the processed data will be stored.
        """
        urls = self.generate_monthly_urls(base_url, year)
        for url in urls:
            csv_path = self.extract_data(url, path)
            self.process_data(csv_path, collection_name)

            zip_name = os.path.join(path, url.split("/")[-1])
            os.remove(zip_name)
