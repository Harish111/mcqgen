import os
import json
import pandas as pd
import traceback

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_and_evaluate_quiz
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langchain.callbacks import get_openai_callback


with open("Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)
    
st.title("Multiple Choice Questions Generator by Harish")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF of Text file")
    
    mcq_count = st.number_input("No. of MCQs",min_value=3, max_value=30)
    
    mcq_subject = st.text_input("Subject", max_chars=20)
    
    mcq_tone = st.text_input("Set the Tone", max_chars=20, placeholder="Simple")
    
    button = st.form_submit_button("Generate MCQs")
    
    if button and uploaded_file is not None and mcq_subject and mcq_count and mcq_tone:
        with st.spinner("Loading.."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response=generate_evaluate_quiz_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject":mcq_subject,
                            "tone": mcq_tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                        )
                    
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
                
            else :
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    quiz =response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")
                    else:
                        st.write(response)
                        
                            
                  