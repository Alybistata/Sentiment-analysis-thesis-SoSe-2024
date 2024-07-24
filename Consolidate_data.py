import pandas as pd
import glob
import os

# Print current working directory
print("Current working directory:", os.getcwd())

# Define the path where your data files are stored
path = 'C:/Users/testf/Desktop/Thesis/Companies'
all_files = glob.glob(os.path.join(path, "*.csv"))  # or "*.csv" for CSV files

# Debugging: Print the list of all files found
print("Files found:", all_files)

# Check if files are found, else print a message
if not all_files:
    print("No files found. Please check the path.")
else:
    # Initialize an empty list to hold DataFrames
    df_list = []

    # Loop through all files and append to the list
    for filename in all_files:
        # Read the CSV file
        df = pd.read_csv(filename)
        
        # Extract company name from the filename (assuming filename is in the format 'companyname_reviews.csv')
        company_name = os.path.basename(filename).split('_')[0]
        
        # Add a new column for the company name
        df['Company'] = company_name
        
        # Combine text fields into a single column
        df['Full Review'] = df['Title'].fillna('') + " | " + df['Main Content'].fillna('')
        
        # Strip leading and trailing whitespace from the 'Full Review' column
        df['Full Review'] = df['Full Review'].str.strip()
        
        # Filter out rows where 'Full Review' is empty
        df = df[df['Full Review'].str.len() > 0]
        
        # Drop unnecessary columns if needed
        df = df.drop(columns=['Title', 'Main Content'])

        # Append the cleaned DataFrame to the list
        df_list.append(df)
    # Concatenate all DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)

    print(combined_df.head())



def convert_star_rating(star_rating):
    return int(star_rating.split(' ')[1])

# Clean and convert star ratings
combined_df['Star Rating'] = combined_df['Star Rating'].apply(convert_star_rating)

# Convert review dates to datetime format
combined_df['Review Date'] = pd.to_datetime(combined_df['Review Date'])


print(combined_df.head())

combined_df.to_csv('consolidated_reviews.csv', index=False)