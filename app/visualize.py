import streamlit as st
from etl.queries import Queries
import pandas as pd
import datetime
import plotly.express as px


queries = Queries("citibike", "trips")

# Streamlit Layout
st.set_page_config(page_title="CitiBike Data Analysis", page_icon=":bike:", layout="wide")
st.title(":bike: CitiBike 2023 Data Analysis And Visualization")
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


with st.sidebar:
    st.sidebar.header('Choose a Query')
    query_type = st.sidebar.selectbox('Select Query', ['User Types',
                                                       'Age and Gender Statistics',
                                                       '...'])

data_col, viz_col = st.columns(2)

if query_type == 'User Types':
    user_types = queries.count_by_user_type()
    user_types_list = list(user_types)
    user_types_df = pd.DataFrame(user_types_list, columns=['count', 'usertype'])  # Ensure column names
    with data_col:
        st.subheader("Data")
        st.dataframe(user_types_df, use_container_width=True, hide_index=True)
    with viz_col:
        fig = px.pie(user_types_df, values='count', names='usertype', title='User Types Visualization',
                     color='usertype', color_discrete_map={'customer': 'red', 'member': 'blue'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

elif query_type == 'User Types(subscribers vs. customers)':
    st.subheader("User Types(subscribers vs. customers)")
    user_types = queries.count_by_user_type()
    st.dataframe(user_types, hide_index=True)

elif query_type == 'Age and Gender Statistics':
    st.subheader("Age and Gender Statistics")
    data = queries.aggregate_by_birth_year_and_gender()
    today = datetime.datetime.now()
    year = today.year
    statistics = []
    for data_point in data:
        if pd.isna(data_point['_id']['birth_year']):
            rider_age = 'Unknown'
        else:
            rider_age = year - int(data_point['_id']['birth_year'])
        rider_gender = data_point['_id']['gender']
        trip_count = data_point['tripCount']
        if rider_gender == 1:
            gender = 'Male'
        elif rider_gender == 2:
            gender = 'Female'
        else:
            gender = 'Unknown'
        statistics.append({"Age": rider_age, "Gender": gender, "Trip Count": trip_count})
    st.dataframe(statistics, hide_index=True)