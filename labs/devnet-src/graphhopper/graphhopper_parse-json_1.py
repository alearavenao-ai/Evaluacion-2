import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Washington, D.C."
loc2 = "Baltimore, Maryland"
key = "8d4d49c4-036b-481c-a7d1-4c3bc9592b98"

url = geocode_url + urllib.parse.urlencode({
    "q": loc1, "limit": 1, "key": key
})

replydata = requests.get(url, timeout=30)
json_data = replydata.json()
json_status = replydata.status_code

print("HTTP status:", json_status)
print(json_data)