import pandas as pd
from google.cloud import storage
import os

# Initialize Google Cloud Storage client
client = storage.Client()

# Specify your bucket name
bucket_name = 'thesis_dataset_hfu'
bucket = client.get_bucket(bucket_name)

# Specify the path and file name in Google Cloud Storage
destination_blob_name = 'path/to/consolidated_reviews.csv'

# Local file to upload
source_file_name = 'consolidated_reviews.csv'

# Function to upload file to GCS
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

# Upload the file
upload_to_gcs(bucket_name, source_file_name, destination_blob_name)