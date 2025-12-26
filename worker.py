
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import json
import os

# Configure logging
logging.basicConfig(
    filename="api_category.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


# Path for the local cache file
CACHE_FILE = "category_cache.json"

# Load cache from file
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# Save cache to file
def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

app = FastAPI()

@app.get("/api/category")
def get_category(request: Request, website: str = Query(..., description="Domain to categorize, e.g. facebook.com")):
    website_key = website.strip().lower()
    cache = load_cache()
    # Check cache first
    if website_key in cache:
        logging.info(f"Cache hit for {website_key}")
        return {"category": cache[website_key], "cached": True}
    url = "https://categorify.org/?utm_source=chatgpt.com"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9,hi;q=0.8",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://categorify.org",
        "priority": "u=0, i",
        "referer": "https://categorify.org/?utm_source=chatgpt.com",
        "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    data = {
        "website": website,
        "try": "Search"
    }
    try:
        client_ip = request.client.host if request.client else "unknown"
        logging.info(f"Request from {client_ip} for website: {website}")
        response = requests.post(url, headers=headers, data=data, timeout=5)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            for box in soup.find_all("div", class_="icon-box"):
                title_span = box.find("span", class_="title")
                if title_span and title_span.text.strip().lower() == "category":
                    category_span = title_span.find_next_sibling("span")
                    if category_span:
                        category = category_span.text.strip()
                        logging.info(f"Category for {website}: {category}")
                        # Store in cache
                        cache[website_key] = category
                        save_cache(cache)
                        return {"category": category, "cached": False}
            logging.warning(f"Category not found in response for {website}")
            return JSONResponse({"error": "Category not found in response."}, status_code=404)
        else:
            logging.error(f"Failed to get category for {website}. Status code: {response.status_code}")
            return JSONResponse({"error": f"Failed to get category. Status code: {response.status_code}"}, status_code=502)
    except Exception as e:
        logging.exception(f"Exception for {website}: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
