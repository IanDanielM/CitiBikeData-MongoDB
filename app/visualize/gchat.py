import google.generativeai as genai
import pandas as pd
import streamlit as st


# Set up the model
def get_response(message: str):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    generation_config = {
        "temperature": 0.5,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

    response = model.generate_content(message, stream=True)

    return response


def analysis_overview(data_type: str, dataframe: pd.DataFrame):
    st.caption("Analysis Overview With Google Gemini AI")
    try:
        user_prompt = """
        Given the following data on Citibike Data, provide an analysis
        that includes a numerical breakdown, percentage distribution,
        and insights into what this data might suggest the trend on the data provided.
        Please analyze the DataFrame provided on our {} and give a comprehensive overview: {}"""
        response_generator = get_response(user_prompt.format(data_type, dataframe))
        with st.chat_message("AI"):
            text_container = st.empty()
            full_text = ""
            for message in response_generator:
                try:
                    full_text += message.text
                    text_container.write(full_text)
                except ValueError:
                    text_container.write(message.text)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return
