import asyncio
import logging

from .thinker_pop_up import create_strava_data_sections_popup, create_strava_activities_sections_popup
from .athlete_api_client import AthleteAPIClient
from .activities_api_client import ActivityAPIClient
from .routes_api_client import RoutesAPIClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIManager:
    def __init__(self, access_token: str):
        """
        Initialize the APIManager with the access token and create API clients.

        :param access_token: The access token for authenticating API requests.
        """
        self.athlete_client = AthleteAPIClient(access_token)
        self.activity_client = ActivityAPIClient(access_token)
        self.routes_client = RoutesAPIClient(access_token)

    def process_activities(self) -> None:
        strava_data_section = create_strava_data_sections_popup()

        ## Athlete
        self.athlete_client.fetch_athlete_data()
        self.athlete_client.save_athlete_data()
        if strava_data_section.get("download_athlete_section"):
            self.athlete_client.fetch_athlete_stats()
            self.athlete_client.save_athlete_states_data()
            # self.athlete_client.fetch_athlete_zone_data()
            # self.athlete_client.save_athlete_zones_data()

        ## Activities
        if strava_data_section.get("download_activities_section"):
            strava_athletes_popup = create_strava_activities_sections_popup()
            self.activity_client.fetch_athlete_activities_data()
            self.activity_client.save_athlete_activities_data()

            if strava_athletes_popup.get("download_activities"):
                asyncio.run(self.activity_client.fetch_and_save_activities_data_async('activities'))
            if strava_athletes_popup.get("download_activities_laps"):
                asyncio.run(self.activity_client.fetch_and_save_activities_data_async('laps'))
            if strava_athletes_popup.get("download_activities_zones"):
                asyncio.run(self.activity_client.fetch_and_save_activities_data_async('zones'))
            if strava_athletes_popup.get("download_activities_comments"):
                asyncio.run(self.activity_client.fetch_and_save_activities_data_async('comments'))
            if strava_athletes_popup.get("download_activities_kudos"):
                asyncio.run(self.activity_client.fetch_and_save_activities_data_async('kudos'))

        ## Section
        # if strava_data_section.get("download_segment_section"):

        ## Routes
        if strava_data_section.get("download_routes_section"):
            self.routes_client.fetch_routes_data()
            self.routes_client.save_routes_data()
            asyncio.run(self.routes_client.fetch_and_save_routes_data_async())
            
        ## Club
        # if strava_data_section.get("download_club_section"):