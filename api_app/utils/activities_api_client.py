import asyncio
import logging
import time
from typing import Dict, Any, Optional

from .base_api_client import BaseAPIClient, RateLimitChecker
from .endpoint_config import StravaEndpoints

class ActivityAPIClient(BaseAPIClient):
    def fetch_athlete_activities_data(self, before: Optional[int] = None, after: Optional[int] = None, page: int = 3, per_page: int = 200) -> Optional[Dict[str, Any]]:
        """
        Fetch athlete Activities data.

        :param before: An epoch timestamp to use for filtering activities that have taken place before a certain time.
        :param after: An epoch timestamp to use for filtering activities that have taken place after a certain time.
        :param page: The page number for pagination.
        :param per_page: The number of activities per page.
        :return: The athlete activities data as a dictionary, or None if an error occurs.
        """
        logging.info("Fetching athlete activities data")
        athlete_activities_url = 'https://www.strava.com/api/v3/athlete/activities'
        self.headers['before'] = str(before)
        self.headers['after'] = str(after)
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

    async def fetch_and_save_activities_data_async(self, data_type: str) -> None:
        """
        Fetch and save Activities data asynchronously.

        :param data_type: Type of activities data to fetch ('activities', 'laps', 'zones', 'comments' or 'kudos')
        """
        start_time = time.time()
        logging.info(f"Starting asynchronous operation to fetch and save activities {data_type} data")

        if self.athlete_activities_data:
            self.activities_ids_list = [activity['id'] for activity in self.athlete_activities_data]
            logging.info(f"Found {len(self.activities_ids_list)} activities in athlete data")
            logging.info(f"Starting asynchronous processing of activities {data_type}")

            remaining_ids = self.activities_ids_list.copy()
            total_requests = len(remaining_ids)
            rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()

            logging.info(f"Rate limit status: {rate_limit_remaining} requests available out of {total_requests} needed")

            endpoint = {
                'activities': StravaEndpoints.ACTIVITIES,
                'laps': StravaEndpoints.ACTIVITIES_LAPS,
                'zones': StravaEndpoints.ACTIVITIES_ZONES,
                'comments': StravaEndpoints.ACTIVITIES_COMMENTS,
                'kudos': StravaEndpoints.ACTIVITIES_KUDOS
            }[data_type]

            while total_requests > rate_limit_remaining:
                start_while_time = time.time()
                logging.info(f"Rate limit reached: Processing {rate_limit_remaining} async requests (pending: {total_requests - rate_limit_remaining})")
                current_ids = remaining_ids[:rate_limit_remaining]
                await asyncio.gather(*(
                    self.process_endpoint(activity_id, endpoint)
                    for activity_id in current_ids
                ))
                logging.info(f"Async processing completed in {time.time() - start_while_time:.2f} seconds")

                current_time = time.localtime()
                wait_minutes = (15 - (current_time.tm_min % 15)) % 15
                wait_seconds = wait_minutes * 60 - current_time.tm_sec

                logging.warning(f"Waiting for {wait_minutes} minutes until next rate limit window")
                await asyncio.sleep(wait_seconds)

                remaining_ids = self.activities_ids_list[rate_limit_remaining:]
                total_requests = len(remaining_ids)
                self.make_readratelimit_api_call()
                rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()
                logging.info(f"New rate limit status: {rate_limit_remaining} requests available")
                logging.info(f"Remaining requests to process: {total_requests}")

            else:
                start_else_time = time.time()
                logging.info(f"Processing {len(remaining_ids if remaining_ids else self.activities_ids_list)} async requests and save data operations")
                await asyncio.gather(*(
                    self.process_endpoint(activity_id, endpoint)
                    for activity_id in remaining_ids
                ))
                logging.info(f"Async processing completed in {time.time() - start_else_time:.2f} seconds")

        elif isinstance(self.athlete_activities_data, (list, dict)) and not self.athlete_activities_data:
            logging.warning(f"No activities {data_type} data to process: Empty dataset received")
        else:
            logging.warning(f"Unable to process activities {data_type}: No data available")

        logging.info(f"Total async processing time: {time.time() - start_time:.2f} seconds")
