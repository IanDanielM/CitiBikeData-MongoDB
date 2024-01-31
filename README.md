# CitiBikeData-MongoDB

This Python script provides an overview for extracting, transforming, and loading (ETL) data into a MongoDB database, along with an extensive set of queries for data analysis. We use the CitiBike Dataset.

## Requirements

- Python 3.x
- Pandas library
- PyMongo library

### Setup

- MongoDB: Ensure MongoDB is installed and running on your system.

- Python Dependencies: Install the required Python libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Extract, Transform, and Load (ETL) Process

CitiBike Provides this dataset in different times or dates. If you wish to change the dataset i used in this example you can download the dataset from [CitiBike](https://s3.amazonaws.com/tripdata/index.html)

## Usage

### ETL Process

- Instantiate the `ExtractLoadTransform Class` and pass the database name and collection name as arguments.

  ```python
  etl = ExtractLoadTransform('citi_bike', 'trips')
  ```

- Extract data from a CSV file and transform it into a list of dictionaries.

  ```python
    data = etl.extract_data('etl/files/201908-citibike-tripdata.csv')
    ```

- Load data into a specified MongoDB collection.

    ```python
    etl.load_data(data)
    ```

### Queries

- Instantiate the `Queries Class` and pass the database name and collection name as arguments.

  ```python
  queries = Queries('citi_bike', 'trips')
  ```

- Retrieve all documents from the collection.

  ```python
    queries.get_all_data()
    ```

- Aggregate by birth year and gender

    ```python
    data = queries.aggregate_by_birth_year_and_gender()
    for record in data:
        print(record)
    ```

## Contributors

- [Ian Daniel Mathenge](https://www.linkedin.com/in/iandanielmathenge/)
