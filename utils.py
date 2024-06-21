import json


def json_load(path):
    info = None
    try:
        info = json.load(open(path))
        print("Successfully loaded", info)
    except Exception as e:
        print("Failed to load level. Error:", e)
    return info