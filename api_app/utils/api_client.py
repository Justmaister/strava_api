import requests
import logging
import os
import json
from typing import Any, Dict, List
from dotenv import load_dotenv

load_dotenv()

class APIClient:
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

    def save_json_to_file(self, data: dict, filename: str):
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)

        file_path = os.path.join(data_dir, filename)

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info("Data saved to %s", file_path)

    def get_athlete_data(self) -> Dict:
        athlete_url = 'https://www.strava.com/api/v3/athlete'
        return self.make_request(athlete_url)

    def get_activities_data(self, page: int = 1, per_page: int = 200) -> Dict:
        athlete_activities_url = 'https://www.strava.com/api/v3/athlete/activities'
        self.headers['page'] = str(page)
        self.headers['per_page'] = str(per_page)
        return self.make_request(athlete_activities_url)

    def extract_activity_ids(self, activities_data) -> List:
        return [activity['id'] for activity in activities_data]