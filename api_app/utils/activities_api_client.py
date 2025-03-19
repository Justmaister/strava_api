import logging
from typing import Dict, Any, Optional
from .base_api_client import BaseAPIClient

class ActivityAPIClient(BaseAPIClient):
    def fetch_athlete_activities_data(self, page: int = 3, per_page: int = 200) -> Optional[Dict[str, Any]]:
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
        self.athlete_activities_data = self.make_request(athlete_activities_url, 'activities')
        return self.athlete_activities_data

    def save_athlete_activities_data(self) -> None:
        """
        Save the fetched athlete activities data to a JSON file.
        """
        if self.athlete_activities_data:
            self.save_json_to_file(self.athlete_activities_data, 'athlete_activities_data.json', 'activities')
        else:
            logging.warning("Athletes Activities data not saved!")

    def fetch_and_save_activities_data(self) -> None:
        """
        Fetch and save individual activities data.
        """
        logging.info("Getting Activities data")
        if self.athlete_activities_data:
            self.activities_ids_list = [activity['id'] for activity in self.athlete_activities_data]
            for activity_id in self.activities_ids_list:
                activity_url = f'https://www.strava.com/api/v3/activities/{activity_id}?include_all_efforts=true'
                self.activity_id_data = self.make_request(activity_url, 'activities')
                if self.activity_id_data:  # Check if data was retrieved successfully
                    self.save_json_to_file(self.activity_id_data, f'activity_{activity_id}.json', 'activities')
                else:
                    logging.warning(f"No data found for Activity ID {activity_id}")
        elif isinstance(self.athlete_activities_data, (list, dict)) and not self.athlete_activities_data:
            logging.warning("Athletes Activities data is empty. Skipping save operation.")
        else:
            logging.warning("Athletes Activities data not found")