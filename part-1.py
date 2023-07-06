import csv
import requests
from bs4 import BeautifulSoup

def scrape_product_listing_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_listings = soup.find_all('div', {'data-component-type': 's-search-result'})
    products = []
    for listing in product_listings:
        product = {}
        url = listing.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')
        product['url'] = 'https://www.amazon.in' + url
        product['name'] = listing.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        price = listing.find('span', {'class': 'a-price-whole'})
        product['price'] = price.text.strip() if price else ''
        rating = listing.find('span', {'class': 'a-icon-alt'})
        product['rating'] = rating.text.strip() if rating else ''
        reviews = listing.find('span', {'class': 'a-size-base'})
        product['reviews'] = reviews.text.strip() if reviews else ''
        products.append(product)
    return products

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
num_pages = 20

all_products = []

page_count = 0

for page in range(1, num_pages + 1):
    url = base_url + str(page)
    products = scrape_product_listing_page(url)
    all_products.extend(products)
    page_count += 1
    if page_count >= num_pages:
        break

csv_file_part1 = 'product_list.csv'

with open(csv_file_part1, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['url', 'name', 'price', 'rating', 'reviews'])
    writer.writeheader()
    writer.writerows(all_products)

print('Part 1: Scraping complete. Data saved to', csv_file_part1)