# CitiBikeData-ETL

## Project Overview

This project aims to perform and ETL Process, analyze and visualize Citibike data using Python, MongoDB, and Streamlit. It provides insights into bike-sharing usage patterns, peak demand times, and station activity, offering valuable information for user behavior analysis, and system optimization.

## Getting Started

### Prerequisites

- Python 3.9 and above
- MongoDB
- OpenAI OR Gemini AI API KEY

### Installation

Clone this repository and install the required Python packages:

```bash
git clone https://github.com/IanDanielM/CitiBikeData-MongoDB.git
cd CitiBikeData-MongoDB
pip install -r requirements.txt
```

### Running the Application

- ETL Process

    Load the data into MongoDB using the `etl.py` script:

    --db: The name of the MongoDB database.

    --collection: The name of the MongoDB collection.

    --uri: The URI for connecting to the MongoDB server.

    --base_url: The base URL for data ingestion.

    --year: The year for filtering the data.

    --file_path: The file path for the data file.

    Example usage:

    ```bash
    python etl.py --db mydatabase --collection mycollection --uri mongodb://localhost:27017 --base_url http://example.com/data --year 2021 --file_path /path/to/data/file
    ```

    This will ingest data from <http://example.com/data>, filter it for the year 2021, and load it into the mycollection collection of the mydatabase database on the MongoDB server running on localhost:27017.

- Visualize the data using the Streamlit dashboard:

    Change the parameter in the `streamlitapp.py` file to match your MongoDB URI, database, and collection.

    ```bash
    streamlit run streamlitapp.py
    ```

    This will start the Streamlit server and open the dashboard in a new browser window.
