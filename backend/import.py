#!/usr/bin/env python3
import sys
import json
import requests

create_url = "http://127.0.0.1:8000/items"

with open(sys.argv[1]) as f:
    data = json.load(f)

for item in data["foods"]:
    print(requests.request("POST", create_url, json=item))
