import requests
import logging
import os
import json
from typing import Any, Dict, List
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    ALLOWED_GROUPS = ['activities', 'routes']
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.access_token}'
        }

    def make_request(self, url: str):
        try:
            logging.info("Sending request to %s", url)
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

    def save_json_to_file(self, data: dict, filename: str, group: str = ''):
        if group and group not in self.ALLOWED_GROUPS:
            raise ValueError(f"Invalid group: {group}. Allowed groups are: {', '.join(self.ALLOWED_GROUPS)}")

        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        if group:
            data_dir = os.path.join(data_dir, group)
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info("Data saved to %s", file_path)

    def fetch_and_save_athlete_data(self):
        athlete_url = 'https://www.strava.com/api/v3/athlete'
        athlete_data = self.make_request(athlete_url)
        if athlete_data:
            self.save_json_to_file(athlete_data, 'athlete_data.json')

    def get_athlete_activities_data(self, page: int = 1, per_page: int = 200) -> Dict:
        athlete_activities_url = 'https://www.strava.com/api/v3/athlete/activities'
        self.headers['page'] = str(page)
        self.headers['per_page'] = str(per_page)
        return self.make_request(athlete_activities_url)

    def fetch_and_save_athlete_activities_data(self, page: int = 1, per_page: int = 200):
        athlete_activities_data = self.get_athlete_activities_data(page=page, per_page=per_page)
        if athlete_activities_data:
            self.save_json_to_file(athlete_activities_data, 'athlete_activities_data.json')

    def fetch_and_save_activities_data(self):
        athlete_activities_data = self.get_athlete_activities_data()
        activities_ids_list = [activity['id'] for activity in athlete_activities_data]
        print(activities_ids_list)
        for activity_id in activities_ids_list:
            activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}?include_all_efforts=true'
            activity_id_data = self.make_request(activity_url)
            self.save_json_to_file(activity_id_data, f'activity_{activity_id}.json', 'activities')
