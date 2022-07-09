#!/usr/bin/env python3
import sys
import json
import urllib.parse
import requests

create_item_url = "http://127.0.0.1:8000/items"
create_tag_url = "http://127.0.0.1:8000/items/{id}/tags/{tag}"

with open(sys.argv[1]) as f:
    data = json.load(f)

categories = {i["id"]: i["name"] for i in data["categories"]}

for item in data["foods"]:
    res = requests.request("POST", create_item_url, json=item)
    print(res)
    #item_id = res.json()["id"]
    #print(requests.request("POST", create_tag_url.format(
    #    id=item_id,
    #    tag=urllib.parse.quote(f"type:{categories[item['category_id']]}"),
    #)))
