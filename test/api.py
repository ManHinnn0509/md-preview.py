import requests as req

from dotenv import load_dotenv
load_dotenv()

import os
token = os.getenv("GITHUB_TOKEN")

h = {}
h["Accept"] = 'application/vnd.github+json'
h["Authorization"] = f"Bearer {token}"
h["X-GitHub-Api-Version"] = "2022-11-28"


url = 'https://api.github.com/markdown'

with open("./README.md", "r", encoding="utf-8") as f:
    s = f.read()

b = {}
b['text'] = s

print(b)

r = req.post(url, headers=h, json=b)

print(r)
print(r.text)
