import pandas as pd
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments

# Load the dataset
data = pd.read_csv('consolidated_reviews.csv')

# Preprocessing: Drop any rows with missing values
data.dropna(inplace=True)

# Encode the star ratings to use as labels
data['Star Rating'] = data['Star Rating'].astype(int)

# Extract relevant columns
reviews = data['Full Review'].tolist()
ratings = data['Star Rating'].tolist()

# Load the tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Tokenize the text
tokens = tokenizer(reviews, padding=True, truncation=True, max_length=512, return_tensors='pt')

# Load the model
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=5)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

# Create a Dataset object
class ReviewDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Create the dataset
dataset = ReviewDataset(tokens, ratings)

# Define the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset,
)

# Train the model
trainer.train()

# Evaluate the model
results = trainer.evaluate()
print(results)
