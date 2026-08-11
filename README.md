# Book Catalog Scraper

A Python script that scrapes book data — title, price, star rating, and stock
availability — from an online catalog and saves it to a clean CSV file.

Built to demonstrate core web scraping skills: handling pagination, parsing
HTML, filtering by category, and exporting structured data.

## Example output

| title                                  | price_gbp | rating_out_of_5 | availability |
|-----------------------------------------|-----------|------------------|--------------|
| A Light in the Attic                    | 51.77     | 3                | In stock     |
| Tipping the Velvet                      | 53.74     | 1                | In stock     |
| Sapiens: A Brief History of Humankind   | 54.23     | 5                | In stock     |

## Features

- Scrapes every page of the catalog automatically (handles pagination)
- Optional `--category` flag to scrape just one category (e.g. "Mystery")
- Optional `--max-pages` flag to limit how many pages are scraped
- Exports results directly to a CSV file
- Sends a proper browser User-Agent header and pauses briefly between
  requests to be respectful of the target server

## How to run it

```bash
pip install requests beautifulsoup4 pandas

python book_scraper.py                        # scrape the entire catalog
python book_scraper.py --category "Mystery"    # scrape just one category
python book_scraper.py --max-pages 3           # limit to first 3 pages
python book_scraper.py --output my_books.csv   # choose the output filename
```

## Built with

- [requests](https://docs.python-requests.org/) — fetching web pages
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — parsing HTML
- [pandas](https://pandas.pydata.org/) — organizing and exporting data
