import requests
import json
import streamlit as st
import pandas as pd
from llama_index.llms.ollama import Ollama as llm

def query(question):
    # Initialize the language model
    llm3 = llm(model="llama3.2:3b", request_timeout=120.0)
    
    # Make a completion request with the question as the prompt
    response = llm3.complete(prompt=question)
    
    # Access the response text directly (adjust attribute based on actual response structure)
    result_text = response.text if hasattr(response, "text") else 'No response available'
    
    return result_text

# Streamlit UI elements
st.header("Welcome to GaneshRaja AI Assistant")
qus = st.text_area("Ask anything")

# Submit button to trigger processing
iocvaluesubmit = st.button("Submit")

if iocvaluesubmit and qus:
    # Process the input question using the query function
    ans = query(qus)
    
    # Option 1: Use `st.write` for better text handling
    st.subheader("Response:")
    st.write(ans)

    # Option 2: Alternatively, use `st.dataframe` with customized column width if needed
    # Convert the answer to a DataFrame (one row for display)
    df = pd.DataFrame([{"Response": ans}])
    st.dataframe(df, width=1000)  # Adjust width as needed for your content