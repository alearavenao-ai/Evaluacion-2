for instruction in path.get("instructions", []):
        text = instruction["text"]
        distance = instruction["distance"]
        print("{0} ( {1:.1f} km / {2:.1f} miles )".format(
            text, distance / 1000, distance / 1000 / 1.61
        ))
    print("=================================================")