import json
import os
import sys 
path = sys.path[0]

def load_msgs(language="English"):
    fpath = f"{path}/messages/msgs_{language}.json"
    if not os.path.exists(fpath):
        fpath = f"{path}/messages/msgs_English.json"
    with open(fpath, "r") as file:
        return (json.load(file))
    