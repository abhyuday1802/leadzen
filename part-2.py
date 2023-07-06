import csv
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product = {}
    asin_tag = soup.find('th', string='ASIN')
    product['asin'] = asin_tag.find_next('td').text.strip() if asin_tag else ''
    description = soup.find('div', {'id': 'productDescription'})
    product['description'] = description.text.strip() if description else ''
    manufacturer = soup.find('a', {'id': 'bylineInfo'})
    product['manufacturer'] = manufacturer.text.strip() if manufacturer else ''
    return product

csv_file_part2 = 'product_data.csv'

base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

all_products_part2 = []

count = 0
page = 1

while count < 200:
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_listings = soup.find_all('div', {'data-component-type': 's-search-result'})
    for listing in product_listings:
        if count >= 200:
            break
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
        additional_info = scrape_product_page(product['url'])
        product.update(additional_info)
        all_products_part2.append(product)
        count += 1
        time.sleep(random.uniform(1, 3))
    page += 1

with open(csv_file_part2, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['url', 'name', 'price', 'rating', 'reviews', 'asin', 'description', 'manufacturer'])
    writer.writeheader()
    writer.writerows(all_products_part2)

print('Part 2: Scraping complete. Data saved to', csv_file_part2)
