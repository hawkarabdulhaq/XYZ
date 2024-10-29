import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Streamlit app title
st.title("Age Filter App")

# Load Google Sheets credentials from secrets
credentials = service_account.Credentials.from_service_account_info(
    json.loads(os.environ["GOOGLE_SHEET_CREDENTIALS_JSON"]),
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

# Define Google Sheets URL and Sheet ID
SPREADSHEET_ID = "1KUHjr6Y9II1GJCqhoQzBj7rCgljFUOnHbK5srHYesMo"
SHEET_NAME = "Sheet1"  # Change this to the actual sheet name if needed

# Function to load data from Google Sheets
def load_data():
    # Access Google Sheets API
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
    data = result.get("values", [])

    # Convert data to a DataFrame
    headers = data[0]  # Assumes first row is header
    rows = data[1:]    # Remaining rows are data
    df = pd.DataFrame(rows, columns=headers)
    
    # Convert numeric columns to appropriate types
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    
    return df

# Function to filter data
def filter_age_data(df):
    return df[df['Age'] > 17]

# Load data and filter it
df = load_data()
filtered_df = filter_age_data(df)

# Display data in Streamlit
st.subheader("Filtered Data (Age > 17)")
st.write(filtered_df)

# Download filtered data as Excel file
@st.cache_data
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="FilteredData")
    processed_data = output.getvalue()
    return processed_data

st.download_button(
    label="Download Filtered Data as Excel",
    data=convert_df_to_excel(filtered_df),
    file_name="filtered_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
