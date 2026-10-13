import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "8d4d49c4-036b-481c-a7d1-4c3bc9592b98"

def geocoding(location, key):
    while not location.strip():
        location = input("Enter the location again (q/quit to exit): ").strip()
    if location.lower() in ("q", "quit"):
        return None, None, None, location
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({
        "q": location, "limit": 1, "key": key
    })
    try:
        replydata = requests.get(url, timeout=30)
    except requests.exceptions.RequestException:
        print("Connection error. Check Internet access and try again.")
        return None, None, None, location
    json_status = replydata.status_code
    try:
        json_data = replydata.json()
    except ValueError:
        print("Geocode API status:", json_status, "Response is not JSON.")
        return json_status, None, None, location
    if json_status == 200 and json_data.get("hits"):
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit.get("name", location)
        state = hit.get("state", "")
        country = hit.get("country", "")
        value = hit.get("osm_value", "unknown")
        new_loc = ", ".join(part for part in (name, state, country) if part)
        print("Geocoding API URL for " + new_loc +
              " (Location Type: " + value + "):\n" + url)
        return json_status, lat, lng, new_loc
    if json_status == 200:
        print("No matches found. Enter a more specific location.")
    else:
        print("Geocode API status:", json_status)
        print("Error message:", json_data.get("message", "Unknown API error"))
    return json_status, None, None, location

while True:
    loc1 = input("Starting Location: ").strip()
    if loc1.lower() in ("q", "quit"):
        break
    orig = geocoding(loc1, key)
    if orig[3].lower() in ("q", "quit"):
        break
    loc2 = input("Destination: ").strip()
    if loc2.lower() in ("q", "quit"):
        break
    dest = geocoding(loc2, key)
    if dest[3].lower() in ("q", "quit"):
        break