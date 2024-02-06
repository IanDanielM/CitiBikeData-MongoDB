import pandas as pd
import streamlit as st
from openai import OpenAI


def get_response(message: str):
    """
    Create a Request to OpenAI

    Args:
        message (str): The user's message.

    Returns:
        completion: The completion object returned by the chatbot model.
                   This object contains the generated response.

    Raises:
        Exception: If an error occurs during the chatbot API call.
    """
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    system_prompt = """
    Given the following data on Citibike Data, provide an analysis
    that includes a numerical breakdown, percentage distribution,
    and insights into what this data might suggest the trend on the data provided
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            stream=True,
        )
        return completion
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return


def analysis_overview(data_type: str, dataframe: pd.DataFrame):
    """
    Generates an analysis overview using OpenAI.

    Parameters:
    - data_type (str): The type of data being analyzed.
    - dataframe: The DataFrame to be analyzed.

    Returns:
    None
    """
    st.caption("Analysis Overview With OpenAI")
    user_prompt = """Please analyze the DataFrame provided on our {} and give a comprehensive overview: {}"""
    try:
        response_generator = get_response(user_prompt.format(data_type, dataframe))

        with st.chat_message("AI"):
            text_container = st.empty()
            full_text = ""
            for response in response_generator:
                if response.choices[0].delta.content:
                    current_text = response.choices[0].delta.content
                    full_text += current_text
                    text_container.write(full_text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
