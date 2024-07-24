import pandas as pd

# Read the CSV file
df = pd.read_csv('category_trust_scores.csv')

# Extract the category name without the page number
df['Category'] = df['Category'].str.split('?').str[0]

# Group by Category and calculate Min, Max, and Avg Trust Scores
grouped_df = df.groupby('Category').agg({'Min Trust Score':'min', 'Max Trust Score':'max', 'Avg Trust Score':'mean'}).reset_index()

# Write the grouped data to a new CSV file
grouped_df.to_csv('category_trust_scores_grouped.csv', index=False)

# Plots
import matplotlib.pyplot as plt

# Plot Min Trust Score
plt.figure(figsize=(10, 5))
plt.bar(grouped_df['Category'], grouped_df['Min Trust Score'], color='blue')
plt.xlabel('Category')
plt.ylabel('Min Trust Score')
plt.title('Minimum Trust Score for Each Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot Max Trust Score
plt.figure(figsize=(10, 5))
plt.bar(grouped_df['Category'], grouped_df['Max Trust Score'], color='green')
plt.xlabel('Category')
plt.ylabel('Max Trust Score')
plt.title('Maximum Trust Score for Each Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot Avg Trust Score
plt.figure(figsize=(10, 5))
plt.bar(grouped_df['Category'], grouped_df['Avg Trust Score'], color='orange')
plt.xlabel('Category')
plt.ylabel('Avg Trust Score')
plt.title('Average Trust Score for Each Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()