import streamlit as st


# Streamlit Layout
def top_bar(queries: object) -> None:
    """
    Display the top bar section of the Streamlit Citibike Data Visualization app.

    Parameters:
    - queries: An object that provides methods to retrieve data from the Citibike dataset.

    Returns:
    None
    """
    try:
        st.title(":bike: CitiBike 2023 Data Analysis And Visualization")
        st.markdown(
            """
        Welcome to Streamlit Citibike Data Visualization, an interactive tool designed
        to explore and analyze the extensive data from New York City's popular
        bike-sharing program.
        Dive into information covering various aspects, from usage patterns to popular routes.
        The app allows you to execute predefined queries or craft your own using the fields in the sidebar.
        Featuring intuitive maps and dynamic charts
            """
        )
        avg_duration = 0
        total_trips = queries.get_total_trips()
        average_trip_duration = queries.get_average_trip_duration()
        for duration in average_trip_duration:
            avg_duration = round((duration["avg_duration"] / 60000), 2)

        first_column, second_column = st.columns(2)
        with first_column:
            st.subheader("Total Trips Covered")
            st.write(f"{total_trips} trips")

        with second_column:
            st.subheader("Average Trip Duration")
            st.write(f"{avg_duration} minutes")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def sidebar_ops(query_type: str) -> str:
    """
    Function to display a sidebar with query options and return the selected query type.

    Parameters:
    query_type (str): The currently selected query type.

    Returns:
    str: The selected query type.

    """
    with st.sidebar:
        st.sidebar.header("Choose a Query")
        query_types = [
            "User Types",
            "Bike Types",
            "Bike Types Used By Members",
            "Popular Stations",
            "Peak Hours",
            "Peak Hours With Day",
            "Total Trips Per Month",
            "Average Trip Duration Per User Types",
            "Average Speed Per User Type and Bike Type",
            "Custom Query",
            "Map Visualization",
        ]
        query_type = st.sidebar.selectbox("Select Query", query_types)

    return query_type
