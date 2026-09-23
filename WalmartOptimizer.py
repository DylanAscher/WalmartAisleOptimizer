import json
import re
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup

def user_info():
    zip_code = input("Enter your zip code: ")
    store_id = input("Enter your Walmart store ID: ")
    return zip_code, store_id

# Getting all Walmart Items #

def get_walmart_items():
    walmart_items = pd.read_csv("allWalmartItems.csv", usecols=["Title", "Pageurl"])
    walmart_items = walmart_items[walmart_items["Pageurl"].notnull()]
    walmart_items = walmart_items[walmart_items["Pageurl"] != ""]
    return walmart_items

def input_item():
    filtered_items = pd.DataFrame(columns=["Pageurl", "Title"])
    while (True):
        item_name = input("Enter the name of the item you want to search for, or type \"Done\" if your grocery list is done: ")
        if item_name.lower() == "done":
            return filtered_items
        walmart_items = get_walmart_items()
        search_terms = re.findall(r"\w+", item_name.lower())
        searchable_text = (
            walmart_items["Title"].fillna("") + " " + walmart_items["Pageurl"].fillna("")
        ).str.lower()
        matching_items = walmart_items[
            searchable_text.map(lambda text: all(term in text for term in search_terms))
        ]
        if matching_items.empty:
            new_item_name = input(f"No item found for '{item_name}'. Please navigate to the Walmart website and copy and paste the EXACT name of the item you want to search for, OR type \"Skip\" to skip this item: ")
            if new_item_name.lower() == "skip":
                continue
            new_item_link = input(f"Now, please copy and past the link leading only up to the item ID. Stop at the question mark (eg. https://www.walmart.com/ip/Great-Value-White-Round-Top-Bread-Loaf-20-oz/10315355): ")
            new_row = pd.DataFrame({
                "Pageurl": [new_item_link],
                "Title": [new_item_name]
            })
            new_row.to_csv('allWalmartItems.csv', mode='a', index=False, header=False)
            print("Added! Please try again.")
            continue
        filtered_items = pd.concat(
            [filtered_items, matching_items], ignore_index=True
        )

# Walmart Request Setup #

def setup_session(zip_code, store_id):
    walmart_session = requests.Session()

    walmart_session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })

    walmart_session.cookies.set("postalCode", zip_code, domain=".walmart.com")

    fulfillment_payload = {
        "postalCode": zip_code,
        "storeId": store_id,
        "deliveryStoreId": store_id,
        "pickupStoreId": store_id,
        "intent": "pickup"
    }
    walmart_session.cookies.set(
        "fulfillmentLocation", 
        json.dumps(fulfillment_payload), 
        domain=".walmart.com"
    )
    return walmart_session

# Getting the Items #

def get_items_helper(item_url, walmart_session):
    if "?" not in item_url:
        item_url += "?intent=pickup"
    else:
        item_url += "&intent=pickup"
    response = walmart_session.get(item_url)
    soup = BeautifulSoup(response.content, "html.parser")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for tag in soup.find_all(True):
        if tag.name == "span" and "Aisle" in tag.text:
            return(tag.text.strip())
            
    return "No aisle found"
        
def get_items(selected_items, walmart_session):
    items_with_aisles = []
    for item in selected_items.itertuples():
        aisle = get_items_helper(item.Pageurl, walmart_session)
        items_with_aisles.append((item.Title, aisle))
    for title, aisle in sorted(items_with_aisles, key=lambda item: item[1]):
        print(f"{title}: {aisle}")

selected_items = input_item()
zip_code, store_id = user_info()
walmart_session = setup_session(zip_code, store_id)
get_items(selected_items, walmart_session)