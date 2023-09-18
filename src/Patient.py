from src.endpoints import Endpoints 
from datetime import datetime, timedelta 
from src.utils import DATE_FMT

class Patient:
    def __init__(self, id, env = "development") -> None:
        self.id = id
        self.ep = Endpoints(env)
        self.language = self.get_patient_language()
        self.slot = self.get_slot() 

    def get_patient_language(self):
        return (self.ep.get_language(patient_id=self.id)["LANGUAGE_KEY"])
        
    def get_slot(self):
        # return an object with 2 attributes
        # start_time, end_time  (both datetimes with today's date)
        time_slot = self.ep.get_time_slot(self.id)
        if len(time_slot) == 0:
            return None
        return (Slot(self.ep.get_time_slot(self.id))) 

    def is_selected_time(self, time):
        if (time > self.slot.start_time) and (time < self.slot.end_time):
            return True
        
        return False
    
    def is_right_after_selected_time(self, time):
        if (time > self.slot.end_time) and (time < self.slot.end_time + timedelta(hours=2)):
            return True
        
        return False

class Slot:
    def __init__(self, slot_dict):
        date = datetime.now().date().strftime("%Y-%m-%d")
        start_datetime = f"{date} {slot_dict['STARTING_TRAINING_TIME']}"
        end_datetime = f"{date} {slot_dict['ENDING_TRAINING_TIME']}"
        self.start_time = datetime.strptime(start_datetime, DATE_FMT)
        self.end_time = datetime.strptime(end_datetime, DATE_FMT)
       