# tools/web_scraper.py
import requests
from bs4 import BeautifulSoup

def main():
    url = input("Enter URL to scrape: ")
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        print("\nWebsite Title:", soup.title.string.strip() if soup.title else "No title found.")
    except Exception as e:
        print("Error:", e)