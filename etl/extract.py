import pandas as pd
from pymongo import MongoClient

client = MongoClient()


class ExtractTransformLoad:
    def __init__(self, db_name: str, collection_name: str = None):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.default_collection = None

        if collection_name:
            self.default_collection = self.get_collection(collection_name)

    def get_collection(self, collection_name: str = None):
        if collection_name:
            return self.db[collection_name]
        elif self.default_collection:
            return self.default_collection
        else:
            raise ValueError("No collection specified")

    def extract_data(self, file_path: str) -> list:
        try:
            df = pd.read_csv(file_path)
            data = df.to_dict("records")  # Transform
            return data
        except Exception as e:
            print(f"Error occurred while extracting data: {e}")
            return []

    def load_data(self, collection_name: str, data: list) -> None:
        try:
            collection = self.get_collection(collection_name)
            collection.insert_many(data)
        except Exception as e:
            print(f"Error occurred while loading data: {e}")
