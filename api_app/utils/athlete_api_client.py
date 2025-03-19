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
        Fetch athlete stats data from the Strava API.

        :return: The athlete stats data as a dictionary, or None if an error occurs.
        """
        logging.info("Getting Athlete Stats data")
        athlete_id = self.athlete_data.get('id')
        athlete_stats_url = f'https://www.strava.com/api/v3/athletes/{athlete_id}/stats'
        self.athlete_states_data = self.make_request(athlete_stats_url, 'Athlete')
        return self.athlete_states_data

    def fetch_athlete_zone_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch athlete zone data from the Strava API.

        :return: The athlete zone data as a dictionary, or None if an error occurs.
        """
        logging.info("Getting Athlete Zones data")
        athlete_zones_url = 'https://www.strava.com/api/v3/athlete/zones'
        self.athlete_zones_data = self.make_request(athlete_zones_url, 'Athlete')
        return self.athlete_zones_data

    def save_athlete_data(self) -> None:
        """
        Save the fetched athlete data to a JSON file.
        """
        if self.athlete_data:
            self.save_json_to_file(self.athlete_data, 'athlete_data.json')
        elif isinstance(self.athlete_data, (list, dict)) and not self.athlete_data:
            logging.warning("Athlete data is empty. Skipping save operation.")
        else:
            logging.warning("Athlete data not saved!")

    def save_athlete_states_data(self) -> None:
        """
        Save the fetched athlete states data to a JSON file.
        """
        if self.athlete_states_data:
            self.save_json_to_file(self.athlete_states_data, 'athlete_states_data.json')
        elif isinstance(self.athlete_states_data, (list, dict)) and not self.athlete_states_data:
            logging.warning("Athlete States data is empty. Skipping save operation.")
        else:
            logging.warning("Athlete States data not saved!")

    def save_athlete_zones_data(self) -> None:
        """
        Save the fetched athlete states data to a JSON file.
        """
        if self.athlete_zones_data:
            self.save_json_to_file(self.athlete_zones_data, 'athlete_zones_data.json')
        elif isinstance(self.athlete_zones_data, (list, dict)) and not self.athlete_zones_data:
            logging.warning("Athlete Zones data is empty. Skipping save operation.")
        else:
            logging.warning("Athlete Zones data not saved!")