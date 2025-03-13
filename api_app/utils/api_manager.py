import logging
from .athlete_api_client import AthleteAPIClient
from .activities_api_client import ActivityAPIClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIManager:
    def __init__(self, access_token: str):
        """
        Initialize the APIManager with the access token and create API clients.

        :param access_token: The access token for authenticating API requests.
        """
        self.athlete_client = AthleteAPIClient(access_token)
        self.activity_client = ActivityAPIClient(access_token)

    def process_activities(self) -> None:
        self.athlete_client.fetch_athlete_data()
        self.athlete_client.save_athlete_data()
        self.activity_client.fetch_athlete_activities_data(page=1, per_page=10)
        self.activity_client.save_athlete_activities_data()
        # self.activity_client.fetch_and_save_activities_data()
