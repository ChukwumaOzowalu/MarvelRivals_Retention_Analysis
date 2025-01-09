from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Set up Selenium WebDriver
driver_path = "C:/Users/eblad/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Replace with your ChromeDriver path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open the Steam reviews page
steam_url = "https://store.steampowered.com/app/2767030/Marvel_Rivals/"  # Replace with the actual URL
driver.get(steam_url)

# Allow time for the page to load
time.sleep(5)

# Scroll down to load reviews
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Locate and scrape reviews
reviews = []
review_elements = driver.find_elements(By.CLASS_NAME, "review_box")  # Adjust class name if necessary
for review in review_elements:
    try:
        user = review.find_element(By.CLASS_NAME, "review_author").text
    except:
        user = "N/A"
    try:
        content = review.find_element(By.CLASS_NAME, "content").text
    except:
        content = "N/A"
    try:
        helpful_count = review.find_element(By.CLASS_NAME, "found_helpful_count").text
    except:
        helpful_count = "N/A"
    reviews.append({"user": user, "content": content, "helpful_count": helpful_count})

# Close the browser
driver.quit()

# Save to a DataFrame
reviews_df = pd.DataFrame(reviews)
reviews_df.to_csv("data/raw/raw_reviews_Rivals.csv", index=False)
print("Scraping complete. Reviews saved to steam_reviews.csv")