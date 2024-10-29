import streamlit as st
import pandas as pd
import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and create a client to access Google Sheets
def authenticate_google_sheets():
    json_creds = os.getenv("GOOGLE_SHEET_CREDENTIALS_JSON")
    
    if json_creds is None:
        st.error("Google Sheets credentials are not configured.")
        return None
    
    try:
        creds_dict = json.loads(json_creds)
        # Set up Google Sheets API scope and credentials
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client
    except json.JSONDecodeError:
        st.error("Failed to parse Google Sheets credentials. Check the format.")
        return None

# Filter data by age
def filter_age():
    client = authenticate_google_sheets()
    if client is None:
        return None

    # Open the Google Sheet by URL
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1KUHjr6Y9II1GJCqhoQzBj7rCgljFUOnHbK5srHYesMo")
    worksheet = sheet.get_worksheet(0)  # Access the first sheet

    # Convert the worksheet data to a DataFrame
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Filter for ages above 17
    filtered_df = df[df['Age'] > 17]

    return filtered_df

# Streamlit app layout
st.title("Age Filter Application")
st.write("This application filters out individuals older than 17 years from a Google Sheet.")

if st.button("Filter and Display Data"):
    filtered_data = filter_age()
    if filtered_data is not None:
        st.write("Filtered Data:")
        st.dataframe(filtered_data)
