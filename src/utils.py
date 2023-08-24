import json
import os
import sys 
path = sys.path[0]

def load_msgs(language="English"):
    fpath = f"{path}/msgs_{language}.json"
    if not os.path.exists(fpath):
        raise ValueError(f"Invalid Language: {language}")
    with open(fpath, "r") as file:
        return (json.load(file))
    