import streamlit as st
import requests
import pandas as pd
from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes

# Initialize OTXv2 with API Key
otx = OTXv2("570baa1d1278af13b033c0cd6c4fc7e510f1c822ca6a5214cd119a9f57acf7d5")  # Replace with your API key

# Define the AlienVault OTX API function for general checks
def alienvault_checker(indicator):
    base_url = 'https://otx.alienvault.com/api/v1/'
    headers = {
        'X-OTX-API-KEY': '570baa1d1278af13b033c0cd6c4fc7e510f1c822ca6a5214cd119a9f57acf7d5'  # Replace with your AlienVault OTX API key
    }
    
    # Determine the type of indicator (IP, domain, hash) and construct the URL
    if "." in indicator and not ":" in indicator:  # Check if it's an IP or domain
        if indicator.replace('.', '').isdigit():
            # It's an IP address
            url = f"{base_url}indicators/IPv4/{indicator}/general"
        else:
            # It's a domain
            url = f"{base_url}indicators/domain/{indicator}/general"
    else:
        # Assume it's a hash
        url = f"{base_url}indicators/file/{indicator}/general"
    
    # Make the API request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("error", "Unknown error occurred.")}

# Function to get Pulse Indicators using OTXv2
def get_pulse_indicators(pulse_id):
    try:
        indicators = otx.get_pulse_indicators(pulse_id)
        return [{"indicator": i["indicator"], "type": i["type"]} for i in indicators]
    except Exception as e:
        return {"error": str(e)}

# Function to get detailed information using OTXv2
def get_indicator_details(indicator_type, indicator):
    try:
        return otx.get_indicator_details_full(indicator_type, indicator)
    except Exception as e:
        return {"error": str(e)}

# Streamlit App Layout
st.title("Threat Intelligence Checker")
st.subheader("Analyze suspicious IPs, URLs, domains, and hashes with OTX")

# Tabs for functionality
tab1, tab2,tab3= st.tabs(["Single Search", "Bulk Search","Pulse Indicators" ])

# Tab 1: Single Search
with tab1:
    st.write("Search for a single IP, URL, domain, or hash:")
    single_input = st.text_input("Enter IP, URL, domain, or hash", "")
    if st.button("Check Single Entry"):
        if single_input.strip():
            with st.spinner("Analyzing..."):
                # Fetch general indicator details
                result = alienvault_checker(single_input.strip())
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Analysis Complete!")
                    st.json(result)
        else:
            st.warning("Please enter a valid input.")

# Tab 2: Bulk Search
with tab2:
    st.write("Upload a file or paste multiple IPs, URLs, domains, or hashes (one per line):")
    uploaded_file = st.file_uploader("Upload a file", type=["txt"])
    bulk_input = st.text_area("Or paste IPs/URLs/domains/hashes below")
    if st.button("Check Bulk Entries"):
        indicator_list = []
        if uploaded_file:
            indicator_list = uploaded_file.read().decode("utf-8").splitlines()
        elif bulk_input.strip():
            indicator_list = bulk_input.splitlines()
        
        if indicator_list:
            with st.spinner("Analyzing entries..."):
                bulk_results = []
                for entry in indicator_list[:1000]:  # Limit to 1000 entries
                    result = alienvault_checker(entry.strip())
                    bulk_results.append(result)
                df = pd.DataFrame(bulk_results)
                st.success("Bulk Analysis Complete!")
                st.dataframe(df)
        else:
            st.warning("Please provide input through a file or text area.")

# Tab 3: Pulse Indicators

with tab3:
    st.write("Retrieve all indicators associated with a specific OTX Pulse ID:")
    pulse_id = st.text_input("Enter Pulse ID", "")
    if st.button("Get Pulse Indicators"):
        if pulse_id.strip():
            with st.spinner("Fetching indicators..."):
                pulse_indicators = get_pulse_indicators(pulse_id.strip())
                if "error" in pulse_indicators:
                    st.error(pulse_indicators["error"])
                else:
                    st.success("Pulse Indicators Retrieved!")
                    df = pd.DataFrame(pulse_indicators)
                    st.dataframe(df)
        else:
            st.warning("Please enter a valid Pulse ID.")

# Footer
st.caption("Powered by GaneshRaja")
