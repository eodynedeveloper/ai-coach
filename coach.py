from datetime import datetime, timedelta
from src.Patient import Patient
from src.utils import load_msgs
from src.Coach import Coach
from src.endpoints import Endpoints
import sys
import logging
import os 

def main():
    os.makedirs(f"{sys.path[0]}/logs", exist_ok=True)
    logging.basicConfig(filename=f'logs/{datetime.now().strftime("%Y-%m-%d_%H_%M")}.log',
                        encoding='utf-8', level=logging.INFO)
    
    # skip for even hours (only run mid session)   
    if datetime.now().hour % 2 == 0:
        return
    
    # initialise logging
    logging.basicConfig(filename=f'{datetime.now().strftime("%Y-%m-%d_%H_%M")}.log',
                        encoding='utf-8', level=logging.DEBUG)
    
    # get session history for all patients
    data = ep.get_history()

    # restructure session history dict
    session_history = dict()
    for i in data:
        session_history[i["PATIENT_ID"]] = i

    # initialize coach 
    coach = Coach(session_history, env=env)
    logging.info('Coach initialized')
    # loop through all patients 
    for patient in session_history.keys():
        print(f"patient ID - {patient}")
        logging.info(f"patient ID - {patient}")

        coach.notif_sent = False
        # get messages in the given language for patient 
        patient = Patient(patient)
        if patient.slot is None:
            continue
        msgs = load_msgs(patient.language)
        coach.msgs = msgs
        personality = coach.calculate_personality(patient.id)
        logging.info(f"selected personality: {personality}")

        # get last session
        last_session = coach.get_last_session(patient.id)

        # schedule all next day reminders at 3AM 
        if datetime.now().hour == 3:
            coach.schedule_session_reminder(patient, personality)
            logging.info("next day reminders scheduled")

        elif last_session is None:
            print("no last session")
            coach.schedule_session_reminder(patient, personality)
            logging.info("next day reminders scheduled")

        # check if current time falls between patient's time slot 
        elif patient.is_selected_time(datetime.now()):
            logging.info("in patient's slot")
            # send reminder if no session done in the last hour
            if last_session.start_time <  datetime.now() - timedelta(minutes=90):
                coach.send_mid_session_reminder(patient.id, personality)
                logging.info("mid session reminder sent")
            
        else:
            logging.info("not in patient's slot")
            # if no sessions since over a day
            if last_session.start_time <  datetime.now() - timedelta(days=1):
                days = (datetime.now() - last_session).days 
                coach.send_not_connected_since_days_reminder(patient.id, personality, days)
                logging.info("not_connected_since_days_reminder_sent")

            # if misses session in decided slot
            elif last_session.start_time < patient.slot.start_time - timedelta(minutes = 30):
                # check streak
                streak_len = coach.get_streak_len(patient.id)
                if streak_len > 0:
                    coach.send_streak_reminder(patient.id, personality, streak_len)
                    logging.info("streak_reminder_sent")
                else:
                    coach.send_out_of_slot_no_streak_reminder(patient.id, personality)
                    logging.info("out_of_slot_no_streak_reminder_sent")

            # TODO: progress reminders 
        



if __name__ == "__main__":
    env = sys.argv[1]
    ep = Endpoints(env)
    main()
    