import random 
from .Patient import Patient 
from .endpoints import Endpoints 
from datetime import datetime, timedelta



class Coach:
    def __init__(self, history, env="development") -> None:
        self.history = history 
        self.notif_sent = False
        self.msgs = None
        self.ep = Endpoints(env)

    def get_last_session(self, patient_id):
        pass 

    def notifs_sent_today(self, patient_id):
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        messages = self.history[patient_id]['MESSAGES']
        n = 0
        for m in messages:
            if datetime.strptime(m['LAUNCH_DATETIME'], date_format).date() == datetime.today.date():
                n+=1
        return n
        
    def select_message(self, msg_list, patient_id):
        patient_history = self.history[patient_id]
        msg_dict = {i:0 for i in msg_list}
        for m in patient_history['MESSAGES']:
            if m["MESSAGE"] in msg_dict:
                msg_dict[m["MESSAGE"]] +=1
        return min(msg_dict, key=msg_dict.get)
    
    def get_streak_len(self, patient_id):
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        patient_history = self.history[patient_id]
        streak_len = 0
        streak = True
        session_dates = [datetime.strptime(i['SESSION_START_TIME'], date_format).date() for i in patient_history['SESSIONS']]
        
        while streak:
            if (datetime.today.date() - timedelta(days=streak_len+1)) in session_dates:
                streak_len +=1
            else:
                streak = False
        return streak_len

    def session_reminder_scheduled(self, patient):
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        patient_history = self.history[patient.id]
        if len(patient_history["MESSAGES"])>0:
            last_message = patient_history["MESSAGES"][-1]
            last_message_time =  datetime.strptime(last_message['LAUNCH_DATETIME'], date_format)
            launch_datetime = (patient.slot.start_time - timedelta(minutes=15))
            if last_message_time == launch_datetime:
                return True
        return False
    
    def calculate_personality(self, patient_id):
        return (random.randint(1, 3)) 
    
    def pick_message(self, patient_id, personality, usecase):
        msg_list = self.msgs[usecase][f'v{personality}']
        return self.select_message(msg_list, patient_id)
    
    def send_mid_session_reminder(self, patient_id, personality):
        message = self.pick_message(patient_id, personality, "mid_session_reminder")
        launch_datetime = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        self.ep.schedule_notif(patient_id, message, launch_datetime, personality)

    def send_not_connected_since_days_reminder(self, patient_id, personality, days=1):
        message = self.pick_message(patient_id, personality, "not_connected_since_days_reminder")
        launch_datetime = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        self.ep.schedule_notif(patient_id, message, launch_datetime, personality)

    def schedule_session_reminder(self, patient, personality):
        if self.session_reminder_scheduled(patient):
            return 
        print("scheduling next day reminder")
        message = self.pick_message(patient.id, personality, "session_reminder")
        launch_datetime = (patient.slot.start_time - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
        print("calling end point")
        self.ep.schedule_notif(patient.id, message, launch_datetime, personality)
        print("endpoint executed")

        
    def send_streak_reminder(self, patient_id, personality, streak_len):
        message = self.pick_message(patient_id, personality, "streak_reminder")
        message.replace(" X", f" {str(streak_len)}")
        message.replace(" x", f" {str(streak_len)}")
        launch_datetime = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        self.ep.schedule_notif(patient_id, message, launch_datetime, personality)

    def send_out_of_slot_no_streak_reminder(self, patient_id, personality):
        message = self.pick_message(patient_id, personality, "out_of_slot_no_streak_reminder")
        launch_datetime = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
        self.ep.schedule_notif(patient_id, message, launch_datetime, personality)

    def send_progress_reminder(self, patient_id, personality):
        pass