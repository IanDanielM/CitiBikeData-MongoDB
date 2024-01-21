import streamlit as st
from etl.queries import Queries
import pandas as pd


queries = Queries("citibike", "trips")

# Streamlit Layout
st.set_page_config(page_title="CitiBike Data Analysis", page_icon=":bike:", layout="wide")
st.title(":bike: CitiBike Data Analysis And Visualization")
st.markdown("""
    This app provides an interactive way to explore Citibike data.
    You can execute various queries to analyze trip data and visualize the results.
    Visualize or Select a query from the sidebar and provide the necessary inputs to get started.
""")

total_trips = queries.get_total_trips()
average_trip_duration = queries.get_average_trip_duration()
for duration in average_trip_duration:
    avg_duration = round((duration['avg_duration'] / 60000), 2)
first_column, second_column = st.columns(2)
with first_column:
    st.subheader("Total Trips Covered")
    st.write(f"{total_trips} trips")

with second_column:
    st.subheader("Average Trip Duration")
    st.write(f"{avg_duration} minutes")

# Example: Display total trips
st.sidebar.header('Choose a Query')
query_type = st.sidebar.selectbox('Select Query', ['Get Data', 'Total Trips', 'Find Bike', '...'])

st.sidebar.header('Visualize Data')
visualize_type = st.sidebar.selectbox('Choose query You want to visualize', ['Get Data', 'Total Trips', 'Find Bike', '...'])

if query_type == 'Get Data':
    page_size = 50
    total_documents = queries.get_data()
    total_pages = total_documents // page_size + (total_documents % page_size > 0)
    page_num = st.sidebar.number_input('Page Number', min_value=1, max_value=total_pages, value=1)

    all_data = queries.get_data(page_num=page_num, page_size=page_size)
    st.table(all_data)
elif query_type == 'Total Trips':
    total_trips = queries.get_total_trips()
    st.write(f"Total Trips: {total_trips}")


if st.sidebar.button("Show Total Trips"):
    total_trips = queries.get_total_trips()
    st.write(f"Total Trips: {total_trips}")


# Example: Visualize some data (adjust according to your data structure)
if st.sidebar.button("Visualize Data"):
    data = queries.get_all_data()
    df = pd.DataFrame(data)
    # Suppose you have a column 'trip_duration'
    st.line_chart(df["tripduration"])
