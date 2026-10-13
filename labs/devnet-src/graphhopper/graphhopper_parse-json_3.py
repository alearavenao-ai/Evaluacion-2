import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "8d4d49c4-036b-481c-a7d1-4c3bc9592b98"

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({
        "q": location, "limit": 1, "key": key
    })
    replydata = requests.get(url, timeout=30)
    json_data = replydata.json()
    json_status = replydata.status_code
    print("Geocoding API URL for " + location + ":\n" + url)
    if json_status == 200 and json_data.get("hits"):
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit.get("name", location)
        state = hit.get("state", "")
        country = hit.get("country", "")
        value = hit.get("osm_value", "unknown")
        new_loc = ", ".join(part for part in (name, state, country) if part)
        print("Location: " + new_loc + " (Location Type: " + value + ")")
        return json_status, lat, lng, new_loc
    print("No coordinates returned:", json_data.get("message", "No matches"))
    return json_status, None, None, location

while True:
    loc1 = input("Starting Location: ").strip()
    if loc1.lower() in ("q", "quit"):
        break
    orig = geocoding(loc1, key)
    print(orig)
    loc2 = input("Destination: ").strip()
    if loc2.lower() in ("q", "quit"):
        break
    dest = geocoding(loc2, key)
    print(dest)