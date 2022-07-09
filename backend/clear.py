#!/usr/bin/env python3
import requests

list_items_url = "http://127.0.0.1:8000/items"
delete_item_url = "http://127.0.0.1:8000/items/{id}"

for item in requests.request("GET", list_items_url).json():
    print(requests.request("DELETE", delete_item_url.format(id=item["id"])))
