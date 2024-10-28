import pandas as pd

# Replace with your Google Sheet URL and sheet name
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1KUHjr6Y9II1GJCqhoQzBj7rCgljFUOnHbK5srHYesMo/export?format=xlsx"

def filter_age():
    # Read data from the Google Sheet
    df = pd.read_excel(GOOGLE_SHEET_URL)

    # Filter for ages above 17
    filtered_df = df[df['Age'] > 17]

    # Save the filtered data to an Excel file
    output_file = 'data/output.xlsx'
    filtered_df.to_excel(output_file, index=False)

    print(f"Filtered data saved to {output_file}")

if __name__ == "__main__":
    filter_age()
