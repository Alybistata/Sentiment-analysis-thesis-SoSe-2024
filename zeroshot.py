import pandas as pd
import emoji

import pandas as pd
import emoji

def replace_emoji_with_description(text):
    """ Replace emojis in the text with their textual descriptions. """
    return emoji.demojize(text, language='alias')

def process_dataset(file_path):
    """ Load the dataset, combine title and main content, process text to replace emojis, and save the processed data. """
    # Load the data
    data = pd.read_csv(file_path)

    # Check if the necessary columns exist
    if 'Title' in data.columns and 'Main Content' in data.columns:
        # Combine 'Title' and 'Main Content' into 'Full Review'
        data['Full Review'] = data['Title'] + " | " + data['Main Content']
        
        # Apply the emoji replacement function to the 'Full Review' column
        data['Full Review'] = data['Full Review'].apply(replace_emoji_with_description)

        # Print the first few rows to verify changes
        print(data.head())

        # Save the processed dataset back to CSV
        data.to_csv('processed_reviews.csv', index=False)
        print("Processed data saved to 'processed_reviews.csv'.")
    else:
        print("Error: Required columns 'Title' and 'Main Content' do not exist in the dataset.")


import pandas as pd
from transformers import pipeline

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Load the data, only the first 5000 rows
df = pd.read_csv("Companies/paypal.com.csv", nrows=5000)

# Define category buckets based on sentiment
positive_labels = ["Fast Delivery", "Good Service", "High Quality", "Great Value", "User-Friendly", "Highly Recommend", "Positive Experience", "Professional Staff", "Clean and Comfortable", "Tasty/Delicious"]
neutral_labels = ["Okay/Decent", "As Expected", "Mixed Feelings", "Acceptable", "No Opinion"]
negative_labels = ["No/Slow Delivery", "Bad Service", "High Price", "Poor Quality", "Difficult to Use", "Won’t Recommend", "Negative Experience", "Unprofessional Staff", "Dirty/Uncomfortable", "Bad Taste/Quality"]

# Function to classify review
def classify_review(row):
    text = row["Full Review"]
    initial_sentiment = row["category"]
    if initial_sentiment == "positive":
        labels = positive_labels
    elif initial_sentiment == "negative":
        labels = negative_labels
    else:
        labels = neutral_labels
    
    # Perform classification
    result = classifier(text, candidate_labels=labels, hypothesis_template="This text is about {}.")
    
    # Sort the results by the highest scores and get the top 3 matches
    top_matches = sorted(zip(result['labels'], result['scores']), key=lambda x: x[1], reverse=True)[:3]
    
    # Print the results
    print(f"Review: {text}\nTop 3 Predicted buckets:")
    for match, score in top_matches:
        print(f"{match} ({score:.2f})")
    
    # Return the best matches as a string
    return ', '.join([f"{match} ({score:.2f})" for match, score in top_matches])

# Apply classification to each row
df["Buckets"] = df.apply(classify_review, axis=1)

# Save the updated dataframe to a new CSV file
df.to_csv("updated_processed_data_subset.csv", index=False)

print("Classification completed and data saved.")
