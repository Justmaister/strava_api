import os
import json
import logging
from typing import Dict, Any, Optional
from .base_api_client import BaseAPIClient

# ATHLETE_FILE = 'api_app/data/athlete_data.json'
ATHLETE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'athlete_data.json')

class RoutesAPIClient(BaseAPIClient):
    def fetch_routes_data(self, page: int = 3, per_page: int = 200) -> Optional[Dict[str, Any]]:
        """
        Fetch routes data from the Strava API.

        :return: The routes data as a dictionary, or None if an error occurs.
        """

        logging.info(f"Loading Athlete ID from {os.path.basename(ATHLETE_FILE)}")
        if os.path.exists(ATHLETE_FILE):
            try:
                with open(ATHLETE_FILE, "r") as file:
                    data = json.load(file)
                    self.id = data.get("id")
                    logging.info(f"Athlete ID succesfully retrieved with the following id: {self.id}")
            except Exception as e:
                logging.error("Error loading token: %s", e)

        logging.info("Getting Routes data")
        routes_url = f'https://www.strava.com/api/v3/athletes/{self.id}/routes'
        self.headers['page'] = str(page)
        self.headers['per_page'] = str(per_page)
        self.routes_data = self.make_request(routes_url, 'Routes')
        return self.routes_data

    def save_routes_data(self) -> None:
        """
        Save the fetched routes data to a JSON file.
        """
        if self.routes_data:
            self.save_json_to_file(self.routes_data, 'routes_data.json', 'routes')
        elif isinstance(self.routes_data, (list, dict)) and not self.routes_data:
            logging.warning("Routes data is empty. Skipping save operation.")
        else:
            logging.warning("Routes data not saved!")