import json

path = "test.json"
sampleInfo = {
    "level":
        {
            "name": "Emma",
            "rollNumber": 5,
        },
    "players":
        {
            "name": "Emma",
            "rollNumber": 5,
        },
    "objects": [
        "object",
        "object",
    ],
}

# Write to json
with open(path, "w") as write:
    json.dump(sampleInfo, write, indent=2)

# Read from json
level_info = json.load(open(path))
print(level_info)
print(level_info["objects"][0])
