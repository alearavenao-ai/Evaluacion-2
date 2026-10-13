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
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles: car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profiles = ["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile (q/quit to exit): ").strip().lower()
    if vehicle in ("q", "quit"):
        break
    if vehicle not in profiles:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using car.")

    loc1 = input("Starting Location: ").strip()
    if loc1.lower() in ("q", "quit"):
        break
    orig = geocoding(loc1, key)
    if orig[3].lower() in ("q", "quit"):
        break
    if orig[0] != 200 or orig[1] is None or orig[2] is None:
        continue

    loc2 = input("Destination: ").strip()
    if loc2.lower() in ("q", "quit"):
        break
    dest = geocoding(loc2, key)
    if dest[3].lower() in ("q", "quit"):
        break
    if dest[0] != 200 or dest[1] is None or dest[2] is None:
        continue

    params = [
        ("key", key),
        ("profile", vehicle),
        ("point", str(orig[1]) + "," + str(orig[2])),
        ("point", str(dest[1]) + "," + str(dest[2])),
        ("instructions", "true"),
        ("locale", "en")
    ]
    paths_url = route_url + urllib.parse.urlencode(params)
    try:
        paths_reply = requests.get(paths_url, timeout=30)
    except requests.exceptions.RequestException:
        print("Connection error. Check Internet access and try again.")
        continue
    paths_status = paths_reply.status_code
    print("=================================================")
    print("Routing API Status:", paths_status)
    print("Routing API URL:\n" + paths_url)
    try:
        paths_data = paths_reply.json()
    except ValueError:
        print("Response is not JSON.")
        continue
    if paths_status != 200:
        print("Error message:", paths_data.get("message", "Unknown API error"))
        print("*************************************************")
        continue
    if not paths_data.get("paths"):
        print("No route returned.")
        continue

    path = paths_data["paths"][0]
    km = path["distance"] / 1000
    miles = km / 1.61
    total_seconds = int(path["time"] / 1000)
    hr = total_seconds // 3600
    minute = (total_seconds // 60) % 60
    sec = total_seconds % 60

    print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
    print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
    print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, minute, sec))
    print("=================================================")

    for instruction in path.get("instructions", []):
        text = instruction["text"]
        distance = instruction["distance"]
        print("{0} ( {1:.1f} km / {2:.1f} miles )".format(
            text, distance / 1000, distance / 1000 / 1.61
        ))
    print("=================================================")