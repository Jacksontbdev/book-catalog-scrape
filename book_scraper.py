"""
Book Catalog Scraper
---------------------
Scrapes book data (title, price, rating, availability) from
books.toscrape.com — a public sandbox site built for practicing
web scraping — and saves the results to a CSV file.

Usage:
    python book_scraper.py
    python book_scraper.py --category "Mystery"
    python book_scraper.py --max-pages 5 --output books.csv
"""

import argparse
import time
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# A real browser User-Agent is good practice — some sites block the default
# "python-requests/x.x" signature outright.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def get_soup(url):
    """Fetch a URL and return a BeautifulSoup object."""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def find_category_url(category_name):
    """Look up the catalogue URL for a given category name."""
    soup = get_soup(BASE_URL)
    links = soup.select(".side_categories ul li ul li a")
    for link in links:
        if link.text.strip().lower() == category_name.strip().lower():
            return BASE_URL + link["href"]
    available = [link.text.strip() for link in links]
    raise ValueError(
        f"Category '{category_name}' not found. Available categories: {available}"
    )


def parse_book_card(card):
    """Extract fields from a single book's <article class='product_pod'>."""
    title = card.h3.a["title"]
    price_text = card.select_one(".price_color").text.strip()
    # Prices look like "£53.74" — strip the currency symbol
    price = float(price_text.replace("£", "").replace("Â", ""))
    rating_class = card.select_one("p.star-rating")["class"]
    rating_word = [c for c in rating_class if c != "star-rating"][0]
    rating = RATING_WORDS.get(rating_word, None)
    availability = card.select_one(".availability").text.strip()
    return {
        "title": title,
        "price_gbp": price,
        "rating_out_of_5": rating,
        "availability": availability,
    }


def scrape(start_url, max_pages=None, delay=0.5):
    """Scrape one or more catalogue pages starting from start_url."""
    results = []
    url = start_url
    page_num = 1

    while url:
        print(f"Scraping page {page_num}: {url}")
        soup = get_soup(url)
        cards = soup.select("article.product_pod")
        for card in cards:
            results.append(parse_book_card(card))

        next_link = soup.select_one("li.next a")
        if next_link and (max_pages is None or page_num < max_pages):
            # Category and root pages have slightly different relative paths
            url = url.rsplit("/", 1)[0] + "/" + next_link["href"]
            page_num += 1
            time.sleep(delay)  # be polite to the server
        else:
            url = None

    return results


def main():
    parser = argparse.ArgumentParser(description="Scrape books.toscrape.com")
    parser.add_argument("--category", help="Only scrape a specific category, e.g. 'Mystery'")
    parser.add_argument("--max-pages", type=int, default=None, help="Limit number of pages scraped")
    parser.add_argument("--output", default="books.csv", help="Output CSV filename")
    args = parser.parse_args()

    if args.category:
        try:
            start_url = find_category_url(args.category)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        start_url = CATALOGUE_URL + "page-1.html"

    books = scrape(start_url, max_pages=args.max_pages)

    df = pd.DataFrame(books)
    df.to_csv(args.output, index=False)
    print(f"\nDone. Scraped {len(df)} books -> saved to {args.output}")
    print(df.head())


if __name__ == "__main__":
    main()
