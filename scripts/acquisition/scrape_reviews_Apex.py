import requests
from bs4 import BeautifulSoup
from datetime import datetime
from random import randint
import pandas as pd
import time

BASE_URL = "https://store.steampowered.com/appreviews/1172470?json=1"  # Replace 12345 with the relevant App ID
max_pages = 10

def scrape_reviews(base_url, max_pages):
    reviews = []  # Initialize an empty list to store reviews
    cursor = "*"  # Initial cursor for pagination

    for page in range(max_pages):
        print(f"Scraping page {page + 1}...")
        
        params = {
            "json": 1,  # Request JSON format for easier parsing
            "cursor": cursor,  # Pagination cursor
            "language": "english",  # Language filter
            "filter": "recent",  # Sort by most recent reviews
        }
        
        # Fetch data from Steam API
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()  # Parse JSON response
        except Exception as e:
            print(f"Error fetching data: {e}. retrying...")
            time.sleep(randint(5, 15))
            continue

        # Debug the API response
        if "reviews" not in data:
            print(f"Unexpected API response: {data}")
            break

        # Append reviews to the list
        for review in data.get("reviews", []):
            print(f"Processing review: {review}")  # Debugging step
            reviews.append({
                "user": review.get("author", {}).get("steamid", "N/A"),
                "content": review.get("review", "N/A"),
                "helpful_count": review.get("votes_up", 0),
                "timestamp": review.get("timestamp_created", None),  # Ensure timestamp is included
                "recommendation": review.get("voted_up", False),  # True = Positive review
            })
        
        # Check for the next cursor
        cursor = data.get("cursor", None)
        if not cursor:
            print("No more pages to scrape.")
            break

        # Respect rate limits
        time.sleep(2)

    if not reviews:
        print("No reviews scraped. Please verify the API response or App ID.")
        return []
    
    print (data)

    return reviews

# Scrape reviews
scraped_reviews = scrape_reviews(BASE_URL, max_pages)

# Convert to DataFrame if reviews exist
if scraped_reviews:
    reviews_df = pd.DataFrame(scraped_reviews)
    reviews_df["timestamp"] = pd.to_datetime(reviews_df["timestamp"], unit="s", errors="coerce")
    reviews_df.to_csv("data/raw/raw_reviews_Apex.csv", index=False)
    print("Scraping complete. Reviews saved to CSV file")
else:
    print("No reviews found.")
    
