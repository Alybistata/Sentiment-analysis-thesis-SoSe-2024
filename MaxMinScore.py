import requests
from bs4 import BeautifulSoup
import time
import csv
from statistics import mean
import re

def scrape_category_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    time.sleep(1)  # Introduce a delay to avoid getting blocked
    soup = BeautifulSoup(response.content, 'html.parser')
    companies = []

    # Find all company cards on the page
    company_cards = soup.find_all('div', class_='paper_paper__1PY90')

    print(f"Number of company cards found on {url}: {len(company_cards)}")

    trust_scores = []

    for card in company_cards:
        company_info = {}
        name_elem = card.find('p', class_='typography_heading-xs__jSwUz')
        trust_score_elem = card.find('span', class_='styles_trustScore__8emxJ')
        reviews_text_elem = card.find('p', class_='typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_ratingText__yQ5S7')

        # Check if all elements exist before accessing their text
        if name_elem and trust_score_elem and reviews_text_elem:
            name = name_elem.text.strip()
            trust_score_text = trust_score_elem.text.strip()
            trust_score = float(re.search(r'\d+\.\d+', trust_score_text).group()) if re.search(r'\d+\.\d+', trust_score_text) else None  # Extract numeric part
            reviews_text = reviews_text_elem.text.strip()
            #num_reviews = int(reviews_text.split()[0].replace(',', ''))

            trust_scores.append(trust_score) if trust_score is not None else None
            companies.append({'Name': name, 'Number of Reviews': "num_reviews", 'Star Rating': trust_score})

    if trust_scores:
        min_trust_score = min(trust_scores)
        max_trust_score = max(trust_scores)
        avg_trust_score = mean(trust_scores)
    else:
        min_trust_score = max_trust_score = avg_trust_score = None

    return {'Category': url.split('/')[-1], 'Min Trust Score': min_trust_score, 'Max Trust Score': max_trust_score, 'Avg Trust Score': avg_trust_score}, companies

# Main function to scrape all categories
def scrape_all_categories():
    categories_file = "trustpilot_categories.csv"
    all_companies = []
    all_category_scores = []

    with open(categories_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            category_link = row['Link']
            page_number = 1

            while True:
                url = f'{category_link}?page={page_number}'
                category_score, companies = scrape_category_page(url)
                if not companies:
                    break
                all_companies.extend(companies)
                all_category_scores.append(category_score)
                page_number += 1

    return all_category_scores, all_companies

# Save data to CSV
def save_to_csv(category_scores, company_details):
    with open('category_trust_scores.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=category_scores[0].keys())
        writer.writeheader()
        writer.writerows(category_scores)

    with open('company_details.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=company_details[0].keys())
        writer.writeheader()
        writer.writerows(company_details)

if __name__ == '__main__':
    category_scores, company_details = scrape_all_categories()
    save_to_csv(category_scores, company_details)
