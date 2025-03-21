import os
import json
import logging
from typing import Dict, Any, Optional

import requests
from dotenv import load_dotenv

# Configure Logging & Load environment variables from .env file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

class APIClient:
    ALLOWED_MODULES = ['activities', 'routes'] # Define allowed modules for saving data

    def __init__(self, access_token: str):
        """
        Initialize the APIClient with an access token.

        :param access_token: The access token for authenticating API requests.
        """
        self.access_token = access_token
        self.headers = {
            'accept': 'application/json', # Specify that we want JSON responses
            'authorization': f'Bearer {self.access_token}' # Set the authorization header
        }

    def make_request(self, url: str, module: str) -> Optional[Dict[str, Any]]:
        """
        Make a GET request to the specified URL and return the JSON response.

        :param url: The URL to send the request to.
        :param module: The name of the module for logging purposes.
        :return: The JSON response as a dictionary, or None if an error occurs.
        """
        try:
            logging.info(f"Sending {module} request to %s", url)
            response = requests.get(url, headers=self.headers) # Send the GET request
            response.raise_for_status() # Raise an error for bad responses (4xx and 5xx)
            logging.info("Request successful")
            return response.json() # Return the JSON response
        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred: %s", http_err)
            return None
        except Exception as err:
            logging.error("An error occurred: %s", err)
            return None

    def save_json_to_file(self, data: dict, filename: str, module: str = '') -> None:
        """
        Save the given data to a JSON file.

        :param data: The data to save.
        :param filename: The name of the file to save the data to.
        :param module: The module name for validation against allowed modules.
        :raises ValueError: If the module is not allowed.
        """
        # Validate the module name if provided
        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        # Define the directory to save the data
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        if module:
            data_dir = os.path.join(data_dir, module)
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        # Write the data to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info("Data saved to %s", file_path)

    #Athlete module
    def fetch_athlete_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch athlete data from the Strava API.

        :return: The athlete data as a dictionary, or None if an error occurs.
        """
        logging.info("Getting Athlete data")
        athlete_url = 'https://www.strava.com/api/v3/athlete'
        self.athlete_data = self.make_request(athlete_url, 'Athlete')
        return self.athlete_data

    def fetch_athlete_activities_data(self, page: int = 1, per_page: int = 200) -> Optional[Dict[str, Any]]:
        """
        Fetch athlete activities data from the Strava API.

        :param page: The page number for pagination.
        :param per_page: The number of activities per page.
        :return: The athlete activities data as a dictionary, or None if an error occurs.
        """
        logging.info("Getting Athlete Activities data")
        athlete_activities_url = 'https://www.strava.com/api/v3/athlete/activities'
        self.headers['page'] = str(page)
        self.headers['per_page'] = str(per_page)
        self.athlete_activities_data = self.make_request(athlete_activities_url, 'Athlete Activities')
        return self.athlete_activities_data

    def save_athlete_and_athlete_activities_data(self) -> None:
        """
        Save the fetched athlete & athlete activities data to a JSON file.
        """
        if self.athlete_data:
            self.save_json_to_file(self.athlete_data, 'athlete_data.json')
        else:
            logging.warning(f"Athlete data not saved!")
        if self.athlete_activities_data:
            self.save_json_to_file(self.athlete_activities_data, 'athlete_activities_data.json')
        else:
            logging.warning("Athletes Activities data not saved!")

    #Activities module
    def fetch_and_save_activities_data(self) -> None:
        """
        Fetch and save individual activities data.
        """
        logging.info("Getting Activities data")
        if self.athlete_activities_data:
            self.activities_ids_list = [activity['id'] for activity in self.athlete_activities_data]
            for activity_id in self.activities_ids_list:
                activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}?include_all_efforts=true'
                self.activity_id_data = self.make_request(activity_url, f'Acivity ID {activity_id}')
                if self.activity_id_data:  # Check if data was retrieved successfully
                    self.save_json_to_file(self.activity_id_data, f'activity_{activity_id}.json', 'activities')
                else:
                    logging.warning(f"No data found for Activity ID {activity_id}")
        else:
            logging.info("Athletes Activities data not found")


    def process_activities(self) -> None:
        self.fetch_athlete_data()
        self.fetch_athlete_activities_data(page=1, per_page=10)
        self.save_athlete_and_athlete_activities_data()

        # self.fetch_and_save_activities_data()

    #Routes module
    def fetch_and_save_routes_data(self):
        try:
            with open(file_path, 'r') as json_file:
                routes_data = json.load(json_file)  # Load the JSON data
                routes_data = self. data
        except Exception as e:
            logging.info("Error opening file. %s", e)
