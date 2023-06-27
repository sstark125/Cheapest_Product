from bs4 import BeautifulSoup
import requests
import re
import urllib3
import os
import pandas as pd

def ConsoleClear():
    os.system('cls' if os.name == 'nt' else 'clear')

ConsoleClear()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

game = input("What game do you want to search for?\n")

url = "https://www.newegg.com/p/pl?d=ps5+games"
page = requests.get(url, verify=False).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])

items_found = {}

for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d=ps5+games&page={page}"
    page = requests.get(url, verify=False).text
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(
        class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell"
    )

    items = div.find_all(string=re.compile(game))
    for item in items:
        parent = item.parent
        link = None
        if parent.name != "a":
            continue

        link = parent["href"]
        next_parent = item.find_parent(class_="item-container")
        try:
            price_element = next_parent.find(class_="price-current")
            if price_element:
                price = price_element.find("strong").get_text(strip=True)
            else:
                price = "N/A"

            items_found[item] = {"price": price, "link": link}
        except:
            pass

sorted_items = sorted(items_found.items(), key=lambda x: x[1]["price"])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]["link"])
    print("----------------------------------------------")
