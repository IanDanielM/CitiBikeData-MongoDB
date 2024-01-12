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

- `ExtractLoadTransform Class` - This class acts as the base class of the ETL process. It contains the following methods: its purpose is to connect to a MongoDB database and perform ETL operations.

  - `__init__(db_name, collection_name)`: Constructor to initialize the database and collection.
  - `get_collection(collection_name)`: Retrieve a specific collection from the database.
  - `extract_data(file_path)`: Extract data from a CSV file and transform it into a list of dictionaries.
  - `load_data(collection_name, data)`: Load data into a specified MongoDB collection.

- `Queries Class` - This class inherits methods from the `ExtractLoadTransform Class`. It acts as an analysis class to execute various queries on the MongoDB collection. methods(queries) used in this class are:

  - `get_all_data()`: Retrieve all documents from the collection.
  - `get_total_trips()`: Count the total number of documents.
  - `find_bike(value)`: Find a specific record by bike ID.
  - `get_unique_start_stations()`: Retrieve unique start station names.
  - `get_average_trip_duration()`: Calculate average trip duration.
  - `get_average_trip_duration_by_bike()`: Calculate average trip duration by bike ID.
  - `sort_by_trip_duration()`: Sort records by trip duration.
  - `filter_by_user_type()`: Filter records by user type.
  - `gender_count()`: Count the number of records by gender.
  - `birth_year_range()`: Find trips by users born in a specific year range.
  - `group_by_start_station()`: Group records by start station.
  - `longest_trips()`: Find the longest trips by duration.
  - `find_same_start_end_stations()`: Find trips where start and end stations are the same.
  - `most_used_bikes()`: List the most frequently used bikes.
  - `distance_covered_by_coordinates()`: Calculate the approximate distance traveled.
  - `total_trips_per_month()`: Count trips made each month.
  - `get_trips_on_specific_date(date)`: Find trips on a specific date.
  - `get_average_trip_duration_by_user_type()`: Calculate average trip duration by user type.
  - `most_popular_stations()`: Find the most popular stations.
  - `aggregate_by_birth_year_and_gender()`: Aggregate data by birth year and gender.

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
