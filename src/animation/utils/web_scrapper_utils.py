import os

import firecrawl
import requests
from dotenv import find_dotenv, load_dotenv


def load_env():
    _ = load_dotenv(find_dotenv())


FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")


def scrape_jina_ai(url: str) -> str:
    response = requests.get("https://r.jina.ai/" + url)
    return response.text


def scrape_firecrawl(url: str):
    app = firecrawl.FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    scraped_data = app.scrape_url(url)["markdown"]
    return scraped_data
