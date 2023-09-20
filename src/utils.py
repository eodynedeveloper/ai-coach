import json
import os
import sys 
from datetime import datetime
path = sys.path[0]


DATETIME_FMT = '%Y-%m-%d %H:%M'

class Slot:
    def __init__(self, slot_dict):
        slot_format = '%Y-%m-%d %H:%M:%S'
        date = datetime.now().date().strftime("%Y-%m-%d")
        start_datetime = f"{date} {slot_dict['STARTING_TRAINING_TIME']}"
        end_datetime = f"{date} {slot_dict['ENDING_TRAINING_TIME']}"
        self.start_time = datetime.strptime(start_datetime, slot_format)
        self.end_time = datetime.strptime(end_datetime, slot_format)
       
class Session:
    def __init__(self, session):
        self.start_time = datetime.strptime(session["STARTING_DATE"], DATETIME_FMT)
        self.score = session['SCORE']
        self.duration = session['SESSION_DURATION_SECONDS']

class Message:
    def __init__(self, message):
        self.message = message["MESSAGE"]
        self.type = message["TYPE"]
        self.time = datetime.strptime(message["LAUNCH_DATETIME"], DATETIME_FMT)
    
        
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