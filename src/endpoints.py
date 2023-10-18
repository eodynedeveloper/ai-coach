import requests 
import logging 

headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7IlBBVElFTlRfSUQiOjIsIkhPU1BJVEFMX0lEIjoxLCJQQVRJRU5UX1VTRVIiOiJzZXJnaSIsIlBBU1NXT1JEIjoiMDU1ZjZmNTE1Yjk1NWE1Yzc3ZjhkNmE4MmQ2ZjBhZWYiLCJDUkVBVElPTl9USU1FIjoiMjAyMi0wMy0yOFQxNTowMjowMi4wMDBaIiwiREVMRVRFX1RJTUUiOm51bGwsIk5BTUUiOm51bGwsIlNVUk5BTUUxIjpudWxsLCJTVVJOQU1FMiI6bnVsbCwiUEFSRVRJQ19TSURFIjoiUklHSFQiLCJVUFBFUl9FWFRSRU1JVFlfVE9fVFJBSU4iOiJSSUdIVCIsIkhBTkRfUkFJU0lOR19DQVBBQ0lUWSI6Ik1FRElVTSIsIkNPR05JVElWRV9GVU5DVElPTl9MRVZFTCI6IkxPVyIsIkhBU19IRU1JTkVHTElHRU5DRSI6MCwiR0VOREVSIjoiTUFMRSIsIlNLSU5fQ09MT1IiOiJGREMzQUQiLCJCSVJUSF9EQVRFIjoiMTk4Ny0wNC0yNlQyMjowMDowMC4wMDBaIiwiVklERU9HQU1FX0VYUCI6bnVsbCwiQ09NUFVURVJfRVhQIjpudWxsLCJDT01NRU5UUyI6bnVsbCwiUFROX0hFSUdIVF9DTSI6MTkzLCJBUk1fU0laRV9DTSI6MjIsIkRFTU8iOjAsIlZFUlNJT04iOjU0LCJpc0NvYWNoQWN0aXZlIjp0cnVlfSwiaWF0IjoxNjkxNTg5MzAyfQ.J5tphIDwZf_2DYJc6YhTl2_AGRowj0b2lbvMkfI2X7c'}

class Endpoints:
    def __init__(self, env = "development", project="global"):
        self.env = env    # development, beta, or production
        if project == "global":
            self.get_history_url = f"https://rgsweb.eodyne.com/rgsmims/backend/{env}/webservices/src/ai-coach/get-patient-messages-and-sessions"
            self.get_time_slot_url = f"https://rgsweb.eodyne.com/rgsmims/backend/{env}/webservices/src/app/2/coach-messages/get-training-time"
            self.schedule_notif_url = f"https://rgsweb.eodyne.com/rgsmims/backend/{env}/webservices/src/ai-coach/add-coach-message"
            self.get_language_url = f"https://rgsweb.eodyne.com/rgsmims/backend/{env}/webservices/src/app/2/patient-language/get"
        elif project == "strack":
            self.get_history_url = f"https://rgsweb.eodyne.com/rgsmims/backend/strack/{env}/src/ai-coach/get-patient-messages-and-sessions"
            self.get_time_slot_url = f"https://rgsweb.eodyne.com/rgsmims/backend/strack/{env}/src/app/2/coach-messages/get-training-time"
            self.schedule_notif_url = f"https://rgsweb.eodyne.com/rgsmims/backend/strack/{env}/src/ai-coach/add-coach-message"
            self.get_language_url = f"https://rgsweb.eodyne.com/rgsmims/backend/strack/{env}/src/app/2/patient-language/get"
        
        else:
            raise Exception("Invalid project: global and strack are the only accepted values")
    
    def get_history(self):
        attempts = 3
        while attempts > 0:
            try:
                response = requests.post(self.get_history_url, headers=headers)
                return (response.json())
            except:
                attempts-=1
                if attempts == 0:
                    raise
        logging.error("get_history end point failed!\nurl:{self.get_history_url}")
        
    
    def get_language(self, patient_id):
        response = requests.get(f"{self.get_language_url}/{patient_id}", headers=headers)
        try:
            return (response.json())
        except:
            return {"LANGUAGE_KEY": "English"}
    
    def get_time_slot(self, patient_id):
        response = requests.get(f"{self.get_time_slot_url}/{patient_id}", headers=headers)
        return (response.json())
    
    def schedule_notif(self, patient_id, message, launch_datetime, coach_personality):
        logging.info(message)
        request_body = {"MESSAGE": message,
                        "LAUNCH_DATETIME" : launch_datetime,
                        "COACH_PERSONALITY": coach_personality}
        print(request_body)
        requests.post(f"{self.schedule_notif_url}/{patient_id}", json=request_body)


