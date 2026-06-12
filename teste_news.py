import requests

API_KEY = "7a1c6708658f493bb44176f431606bc3"

url = "https://newsapi.org/v2/everything"

params = {
    "q": "luxury",
    "language": "en",
    "pageSize": 3,
    "apiKey": API_KEY
}

r = requests.get(url, params=params)

print("STATUS:", r.status_code)
print()
print(r.text[:1000])
