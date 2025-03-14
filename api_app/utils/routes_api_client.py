import logging
from typing import Dict, Any, Optional
from .base_api_client import BaseAPIClient

class RoutesAPIClient(BaseAPIClient):
    def fetch_routes_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch routes data from the Strava API.

        :return: The routes data as a dictionary, or None if an error occurs.
        """
        logging.info("Getting Routes data")
        routes_url = 'https://www.strava.com/api/v3/routes'
        self.routes_data = self.make_request(routes_url, 'Routes')
        return self.routes_data

    def save_routes_data(self) -> None:
        """
        Save the fetched routes data to a JSON file.
        """
        if self.routes_data:
            self.save_json_to_file(self.routes_data, 'routes_data.json')
        else:
            logging.warning("Routes data not saved!")