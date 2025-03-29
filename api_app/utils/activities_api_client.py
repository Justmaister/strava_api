import asyncio
import logging
import time
from typing import Dict, Any, Optional

from .base_api_client import BaseAPIClient, RateLimitChecker
from .endpoint_config import StravaEndpoints

class ActivityAPIClient(BaseAPIClient):
    def fetch_athlete_activities_data(self, page: int = 3, per_page: int = 200) -> Optional[Dict[str, Any]]:
        """
        Fetch athlete Activities data.

        :param page: The page number for pagination.
        :param per_page: The number of activities per page.
        :return: The athlete activities data as a dictionary, or None if an error occurs.
        """
        logging.info("Fetching athlete activities data")
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
            logging.warning("Unable to save athlete activities data: No data available")

    async def fetch_and_save_activities_data_async(self) -> None:
        """
        Fetch and save Activities data asynchronously.
        """
        start_time = time.time()
        logging.info("Starting asynchronous operation to fetch and save activities data")

        if self.athlete_activities_data:
            self.activities_ids_list = [activity['id'] for activity in self.athlete_activities_data]
            logging.info(f"Found {len(self.activities_ids_list)} activities in athlete data")
            logging.info("Starting asynchronous processing of activities")

            remaining_ids = self.activities_ids_list.copy()
            total_requests = len(remaining_ids)
            rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()

            logging.info(f"Rate limit status: {rate_limit_remaining} requests available out of {total_requests} needed")

            while total_requests > rate_limit_remaining:
                start_while_time = time.time()
                logging.info(f"Rate limit reached: Processing {rate_limit_remaining} async requests (pending: {total_requests - rate_limit_remaining})")
                current_urls = remaining_ids[:rate_limit_remaining]
                await asyncio.gather(*(
                    self.process_activity(activity_id, StravaEndpoints.ACTIVITIES)
                    for activity_id in current_urls
                ))
                logging.info(f"Async processing completed in {time.time() - start_while_time:.2f} seconds")

                # Calculate wait time until the next 15-minute interval
                current_time = time.localtime()
                wait_minutes = (15 - (current_time.tm_min % 15) + 1) % 15
                wait_seconds = wait_minutes * 60 - current_time.tm_sec

                logging.warning(f"Waiting for {wait_minutes} minutes until next rate limit window")
                await asyncio.sleep(wait_seconds)  # Wait until the next interval

                remaining_ids = self.activities_ids_list[rate_limit_remaining:]  # Get the remaining URLs
                total_requests = len(remaining_ids)
                self.make_readratelimit_api_call()
                rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()
                logging.info(f"New rate limit status: {rate_limit_remaining} requests available")
                logging.info(f"Remaining requests to process: {total_requests}")

            else:
                start_else_time = time.time()
                logging.info(f"Processing {len(remaining_ids if remaining_ids else self.activities_ids_list)} async requests and save data operations")
                await asyncio.gather(*(
                    self.process_activity(activity_id, StravaEndpoints.ACTIVITIES)
                    for activity_id in remaining_ids
                ))
                logging.info(f"Async processing completed in {time.time() - start_else_time:.2f} seconds")

        elif isinstance(self.athlete_activities_data, (list, dict)) and not self.athlete_activities_data:
            logging.warning("No activities data to process: Empty dataset received")
        else:
            logging.warning("Unable to process activities: No data available")

        logging.info(f"Total async processing time: {time.time() - start_time:.2f} seconds")

    async def fetch_and_save_activities_laps_data_async(self) -> None:
        """
        Fetch and save Activities Laps data asynchronously.
        """

        start_time = time.time()

        logging.info("Fetching Activities Laps data asynchronously")
        if self.athlete_activities_data:
            self.activities_ids_list = [activity['id'] for activity in self.athlete_activities_data]

            urls = [f'https://www.strava.com/api/v3/activities/{activity_id}/laps'
                   for activity_id in self.activities_ids_list]
            activities_data = await asyncio.gather(*(self.make_async_request(url, 'activities') for url in urls))

            for activity_id, activity_data in zip(self.activities_ids_list, activities_data):
                if activity_data:
                    self.save_json_to_file(activity_data, f'activity_{activity_id}_laps.json', 'activities')
                else:
                    logging.warning(f"No Laps data found for Activity ID {activity_id}")
        elif isinstance(self.athlete_activities_data, (list, dict)) and not self.athlete_activities_data:
            logging.warning("Athletes Activities data is empty. Skipping save operation.")
        else:
            logging.warning("Athletes Activities Laps data not found")

        logging.info(f"Async sync code cost {time.time() - start_time:.2f} seconds")

    async def fetch_and_save_activities_zones_data_async(self) -> None:
        """
        Fetch and save Activities Zones data asynchronously.
        """

        start_time = time.time()

        logging.info("Fetching Activities Zones data asynchronously")
        if self.athlete_activities_data:
            self.activities_ids_list = [activity['id'] for activity in self.athlete_activities_data]

            urls = [f'https://www.strava.com/api/v3/activities/{activity_id}/zones'
                   for activity_id in self.activities_ids_list]
            activities_data = await asyncio.gather(*(self.make_async_request(url, 'activities') for url in urls))

            for activity_id, activity_data in zip(self.activities_ids_list, activities_data):
                if activity_data:
                    self.save_json_to_file(activity_data, f'activity_{activity_id}_zones.json', 'activities')
                else:
                    logging.warning(f"No Zones data found for Activity ID {activity_id}")
        elif isinstance(self.athlete_activities_data, (list, dict)) and not self.athlete_activities_data:
            logging.warning("Athletes Activities data is empty. Skipping save operation.")
        else:
            logging.warning("Athletes Activities Zones data not found")

        logging.info(f"Async sync code cost {time.time() - start_time:.2f} seconds")