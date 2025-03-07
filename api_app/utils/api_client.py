import requests
import logging
import os
import json
from typing import Any, Dict, List
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    ALLOWED_MODULES = ['activities', 'routes']
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.access_token}'
        }

    def make_request(self, url: str, module: str):
        try:
            logging.info(f"Sending {module} request to %s", url)
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logging.info("Request successful")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred: %s", http_err)
            return None
        except Exception as err:
            logging.error("An error occurred: %s", err)
            return None

    def save_json_to_file(self, data: dict, filename: str, module: str = ''):
        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        if module:
            data_dir = os.path.join(data_dir, module)
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info("Data saved to %s", file_path)

    #Athlete module
    def fetch_athlete_data(self):
        logging.info("Getting Athlete data")
        athlete_url = 'https://www.strava.com/api/v3/athlete'
        self.athlete_data = self.make_request(athlete_url, 'Athlete')
        return self.athlete_data

    def save_athlete_data(self):
        if self.athlete_data:
            self.save_json_to_file(self.athlete_data, 'athlete_data.json')
        else:
            logging.warning(f"Athlete data not loaded")

    #Activities module
    def fetch_athlete_activities_data(self, page: int = 1, per_page: int = 200) -> Dict:
        logging.info("Getting Athlete Activities data")
        athlete_activities_url = 'https://www.strava.com/api/v3/athlete/activities'
        self.headers['page'] = str(page)
        self.headers['per_page'] = str(per_page)
        self.athlete_activities_data = self.make_request(athlete_activities_url, 'Athlete Activities')
        return self.athlete_activities_data

    def save_athlete_activities_data(self):
        if self.athlete_activities_data:
            self.save_json_to_file(self.athlete_activities_data, 'athlete_activities_data.json')
        else:
            logging.warning("Athletes Activities data not loaded")

    def fetch_and_save_activities_data(self):
        logging.info("Getting Activities data")
        if self.athlete_activities_data:
            self.activities_ids_list = [activity['id'] for activity in self.athlete_activities_data]
            for activity_id in self.activities_ids_list:
                activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}?include_all_efforts=true'
                self.activity_id_data = self.make_request(activity_url, f'Acivity {activity_id}')
                self.save_json_to_file(self.activity_id_data, f'activity_{activity_id}.json', 'activities')
        else:
            logging.info("Athletes Activities data not found")


    def process_activities(self):
        self.fetch_athlete_data()
        self.save_athlete_data()

        self.fetch_athlete_activities_data(page=1, per_page=10)
        self.save_athlete_activities_data()

        self.fetch_and_save_activities_data()

    #Routes module
    def fetch_and_save_routes_data(self):
        try:
            with open(file_path, 'r') as json_file:
                routes_data = json.load(json_file)  # Load the JSON data
                routes_data = self. data
        except Exception as e:
            logging.info("Error opening file. %s", e)
