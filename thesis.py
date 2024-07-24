import requests
from bs4 import BeautifulSoup
import csv
import time  # Import the time module

# Define the base URL
base_url = "https://www.trustpilot.com/review/www.homedepot.com?page="

# Create a list to store the reviews
all_reviews = []

# Loop through pages from 1 to 2500
for page_num in range(1, 1000):
    # Construct the URL for the current page
    url = base_url + str(page_num)
    
    # Request the page content
    print("Requesting page:", url)
    page = requests.get(url)

    # Check if the page was successfully retrieved
    if page.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(page.content, "html.parser")

        # Find all review elements
        reviews = soup.find_all(class_="paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv card_noPadding__D8PcU styles_reviewCard__hcAvl")

        # Loop through each review element
        for review in reviews:
            review_info = {}
            # Extract title
            title = review.find(class_="link_internal__7XN06 typography_appearance-default__AAY17 typography_color-inherit__TlgPO link_link__IZzHN link_notUnderlined__szqki")
            if title:
                review_info['Title'] = title.text.strip()

            # Extract img alt from star rating
            star_rating_img = review.find(class_="star-rating_starRating__4rrcf star-rating_medium__iN6Ty").find('img')
            if star_rating_img:
                review_info['Star Rating'] = star_rating_img.get('alt')

            # Extract main content
            main_content = review.find(class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn")
            if main_content:
                review_info['Main Content'] = main_content.text.strip()

            # Extract review date
            review_date = review.find('time', class_="")
            if review_date:
                review_info['Review Date'] = review_date.get('datetime')

            print(review_info)

            # Add review_info to the list of all_reviews
            all_reviews.append(review_info)
            
        # Introduce a delay of 5 seconds before making the next request
        time.sleep(3)

# Sort reviews by date from newest to oldest
all_reviews_sorted = sorted(all_reviews, key=lambda x: x.get('Review Date'), reverse=True)

# Define the CSV file name
csv_file = "homedepot.com.csv"

# Define the CSV fieldnames
fieldnames = ['Title', 'Star Rating', 'Main Content', 'Review Date']

# Write the reviews to a CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_reviews_sorted)

print("CSV file generated successfully.")
