import logging
from typing import Dict, Any, Optional
from .base_api_client import BaseAPIClient

class AthleteAPIClient(BaseAPIClient):
    def fetch_athlete_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch athlete data from the Strava API.

        :return: The athlete data as a dictionary, or None if an error occurs.
        """
        logging.info("Getting Athlete data")
        athlete_url = 'https://www.strava.com/api/v3/athlete'
        self.athlete_data = self.make_request(athlete_url, 'Athlete')
        return self.athlete_data

    def fetch_athlete_stats(self) -> Optional[Dict[str, Any]]:
        """
        Fetch athlete data from the Strava API.

        :return: The athlete data as a dictionary, or None if an error occurs.
        """
        logging.info("Getting Athlete Stats data")
        athlete_id = self.athlete_data.get('id')
        athlete_url = f'https://www.strava.com/api/v3/athletes/{athlete_id}/stats'
        self.athlete_states_data = self.make_request(athlete_url, 'Athlete')
        return self.athlete_states_data

    def save_athlete_data(self) -> None:
        """
        Save the fetched athlete data to a JSON file.
        """
        if self.athlete_data:
            self.save_json_to_file(self.athlete_data, 'athlete_data.json')
        elif isinstance(self.athlete_data, (list, dict)) and not self.athlete_data:
            logging.info("Routes data is empty. Skipping save operation.")
        else:
            logging.warning("Athlete data not saved!")

    def save_athlete_states_data(self) -> None:
        """
        Save the fetched athlete data to a JSON file.
        """
        if self.athlete_states_data:
            self.save_json_to_file(self.athlete_states_data, 'athlete_states_data.json')
        elif isinstance(self.athlete_states_data, (list, dict)) and not self.athlete_states_data:
            logging.info("Routes data is empty. Skipping save operation.")
        else:
            logging.warning("Athlete data not saved!")