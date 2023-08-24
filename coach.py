from datetime import datetime, timedelta
from src.Patient import Patient
from src.utils import load_msgs
from src.Coach import Coach
from src.endpoints import Endpoints
import sys

def main():    
    # get session history for all patients
    data = ep.get_history()

    # restructure session history dict
    session_history = dict()
    for i in data:
        session_history[i["PATIENT_ID"]] = i

    # initialize coach 
    coach = Coach(session_history, env=env)
    # loop through all patients 
    for patient in session_history.keys():
        coach.notif_sent = False
        # get messages in the given language for patient 
        patient = Patient(patient)
        if patient.slot is None:
            continue
        msgs = load_msgs(patient.language)
        coach.msgs = msgs
        personality = coach.calculate_personality(patient.id)
        print(personality)
        # get last session
        last_session = coach.get_last_session(patient.id)

        if last_session is None:
            print("no last session")
            coach.schedule_next_day_reminder(patient, personality)
            
        # check if current time falls between patient's time slot 
        elif patient.is_selected_time(datetime.now()):
            print("in patient's slot")
            # send reminder if no session done in the last hour
            if last_session.start_time <  datetime.now() - timedelta(minutes=90):
                coach.send_mid_session_reminder(patient.id, personality)
            else:
                coach.schedule_next_day_reminder(patient, personality)
        else:
            print("not in patient's slot")
            # if no sessions since over a day
            if last_session.start_time <  datetime.now() - timedelta(days=1):
                days = (datetime.now() - last_session).days 
                coach.send_not_connected_since_days_reminder(patient.id, personality, days)

            # if misses session in decided slot
            elif last_session.start_time < patient.slot.start_time - timedelta(minutes = 30):
                # check streak
                streak_len = coach.get_streak_len(patient.id)
                if streak_len > 0:
                    coach.send_streak_reminder(patient.id, personality, streak_len)
                else:
                    coach.send_out_of_slot_no_streak_reminder(patient.id, personality)
            
            # if does a session in the decided time slot
            elif ((last_session.start_time > patient.slot.start_time - timedelta(minutes = 30)) and (last_session.start_time < patient.slot.end_time + timedelta(minutes = 30))):
                coach.schedule_next_day_reminder(patient, personality)
            
            # TODO: progress reminders 
        



if __name__ == "__main__":
    env = sys.argv[1]
    ep = Endpoints(env)
    main()
    