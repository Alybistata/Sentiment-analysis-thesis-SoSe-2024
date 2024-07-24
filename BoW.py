import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# Load the data from the CSV file
df = pd.read_csv("trustpilot_reviews_westernunion_big.csv")

# Drop rows with missing values in the 'Main Content' column
df.dropna(subset=['Main Content'], inplace=True)

# Tokenize the text
documents = df['Main Content']

# Initialize TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')

# Fit and transform the data
tfidf = tfidf_vectorizer.fit_transform(documents)

# Initialize NMF
num_topics = 5  # Number of topics to extract
nmf_model = NMF(n_components=num_topics, random_state=42)

# Fit the model
nmf_model.fit(tfidf)

# Print the topics and their top keywords
feature_names = tfidf_vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(nmf_model.components_):
    print(f"Topic {topic_idx+1}:")
    print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))
