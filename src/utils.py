import json
import os
import sys 
from src.Coach import Session
path = sys.path[0]

def load_msgs(language="English"):
    fpath = f"{path}/messages/msgs_{language}.json"
    if not os.path.exists(fpath):
        fpath = f"{path}/messages/msgs_English.json"
    with open(fpath, "r") as file:
        return (json.load(file))

def default_last_session():
    last_session = {'STARTING_DATE': '2000-01-01 17:00',
                    'SCORE': 100,
                    'SESSION_DURATION_SECONDS': 100}
    
    return Session(last_session)