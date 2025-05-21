import os
import json
import logging
import asyncio
import time
from typing import Dict, Any, Optional

from .base_api_client import BaseAPIClient, RateLimitChecker
from .endpoint_config import StravaEndpoints

ATHLETE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'athlete_data.json')

class ClubsAPIClient(BaseAPIClient):
    def fetch_clubs_data(self, page: int = 3, per_page: int = 200) -> Optional[Dict[str, Any]]:
        """
        Fetch clubs data from the Strava API.

        :param page: The page number for pagination.
        :param per_page: The number of clubs per page.
        :return: The clubs data as a dictionary, or None if an error occurs.
        """
        logging.info("Fetching athlete clubs data")

        logging.info(f"Loading Athlete ID from {os.path.basename(ATHLETE_FILE)}")
        if os.path.exists(ATHLETE_FILE):
            try:
                with open(ATHLETE_FILE, "r") as file:
                    data = json.load(file)
                    self.id = data.get("id")
                    logging.info(f"Athlete ID succesfully retrieved with the following id: {self.id}")
            except Exception as e:
                logging.error("Error loading token: %s", e)

        logging.info("Fetching Clubs data")
        clubs_url = f'https://www.strava.com/api/v3/athlete/clubs'
        self.headers['page'] = str(page)
        self.headers['per_page'] = str(per_page)
        self.clubs_data = self.make_request(clubs_url, 'clubs')
        return self.clubs_data

    def save_clubs_data(self) -> None:
        """
        Save the fetched clubs data to a JSON file.
        """
        if self.clubs_data:
            self.save_json_to_file(self.clubs_data, 'clubs_data.json', 'clubs')
        elif isinstance(self.clubs_data, (list, dict)) and not self.clubs_data:
            logging.warning("Clubs data is empty. Skipping save operation.")
        else:
            logging.warning("Clubs data not saved!")

    async def fetch_and_save_clubs_data_async(self, data_type: str) -> None:
        """
        Fetch and save Clubs data asynchronously.

        :param data_type: Type of clubs data to fetch ('clubs', 'members', or 'activities')
        """
        start_time = time.time()
        logging.info(f"Starting asynchronous operation to fetch and save clubs {data_type} data")

        if self.clubs_data:
            self.clubs_ids_list = [club['id'] for club in self.clubs_data]
            logging.info(f"Found {len(self.clubs_ids_list)} clubs in athlete data")
            logging.info(f"Starting asynchronous processing of clubs {data_type}")

            remaining_ids = self.clubs_ids_list.copy()
            total_requests = len(remaining_ids)
            rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()

            logging.info(f"Rate limit status: {rate_limit_remaining} requests available out of {total_requests} needed")

            # Determine the appropriate endpoint based on data_type
            endpoint = {
                'clubs': StravaEndpoints.CLUBS,
                'members': StravaEndpoints.CLUB_MEMBERS,
                'activities': StravaEndpoints.CLUB_ACTIVITIES
            }[data_type]

            while total_requests > rate_limit_remaining:
                start_while_time = time.time()
                logging.info(f"Rate limit reached: Processing {rate_limit_remaining} async requests (pending: {total_requests - rate_limit_remaining})")
                current_ids = remaining_ids[:rate_limit_remaining]
                await asyncio.gather(*(
                    self.process_endpoint(club_id, endpoint)
                    for club_id in current_ids
                ))
                logging.info(f"Async processing completed in {time.time() - start_while_time:.2f} seconds")

                current_time = time.localtime()
                wait_minutes = (15 - (current_time.tm_min % 15)) % 15
                wait_seconds = wait_minutes * 60 - current_time.tm_sec

                logging.warning(f"Waiting for {wait_minutes} minutes until next rate limit window")
                await asyncio.sleep(wait_seconds)

                remaining_ids = self.clubs_ids_list[rate_limit_remaining:]
                total_requests = len(remaining_ids)
                self.make_readratelimit_api_call()
                rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()
                logging.info(f"New rate limit status: {rate_limit_remaining} requests available")
                logging.info(f"Remaining requests to process: {total_requests}")

            else:
                start_else_time = time.time()
                logging.info(f"Processing {len(remaining_ids if remaining_ids else self.clubs_ids_list)} async requests and save data operations")
                await asyncio.gather(*(
                    self.process_endpoint(club_id, endpoint)
                    for club_id in remaining_ids
                ))
                logging.info(f"Async processing completed in {time.time() - start_else_time:.2f} seconds")

        elif isinstance(self.clubs_data, (list, dict)) and not self.clubs_data:
            logging.warning(f"No clubs {data_type} data to process: Empty dataset received")
        else:
            logging.warning(f"Unable to process clubs {data_type}: No data available")

        logging.info(f"Total async processing time: {time.time() - start_time:.2f} seconds")
