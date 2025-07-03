# ✅ scraping/mosdac_scraper.py

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import logging
from urllib.parse import urljoin, urlparse
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def scrape_mosdac(base_url, depth=1):
    visited = set()
    scraped_texts = []
    url_queue = [(base_url, 0)]

    with tqdm(total=1, desc="Scraping", unit="page") as pbar:
        while url_queue:
            url, current_depth = url_queue.pop(0)
            if current_depth > depth or url in visited:
                continue

            try:
                response = requests.get(url, timeout=10)
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    continue

                visited.add(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = clean_text(soup.get_text())
                if text:
                    scraped_texts.append(text)

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if 'mosdac.gov.in' in full_url and is_valid_url(full_url) and full_url not in visited:
                        url_queue.append((full_url, current_depth + 1))

                time.sleep(1)  # Be polite
                pbar.total += 1
                pbar.update(1)
            except Exception as e:
                logging.warning(f"Failed to scrape {url}: {e}")

    return scraped_texts

def save_scraped_data(scraped_data, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'w', encoding='utf-8') as f:
        for entry in scraped_data:
            f.write(entry + '\n\n')

if __name__ == '__main__':
    base_url = 'https://www.mosdac.gov.in/'
    output_file = 'data/raw_scraped.txt'
    logging.info("🔍 Starting MOSDAC scraping...")
    data = scrape_mosdac(base_url, depth=1)
    save_scraped_data(data, output_file)
    logging.info(f"✅ Scraping complete. Data saved to {output_file}")
