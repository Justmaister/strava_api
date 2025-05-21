import os
import json
import logging
import asyncio
import time
from typing import Dict, Any, Optional

from .base_api_client import BaseAPIClient, RateLimitChecker
from .endpoint_config import StravaEndpoints

ATHLETE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'athlete_data.json')

class RoutesAPIClient(BaseAPIClient):
    def fetch_routes_data(self, page: int = 3, per_page: int = 200) -> Optional[Dict[str, Any]]:
        """
        Fetch routes data from the Strava API.

        :param page: The page number for pagination.
        :param per_page: The number of routes per page.
        :return: The routes data as a dictionary, or None if an error occurs.
        """
        logging.info("Fetching athlete routes data")

        logging.info(f"Loading Athlete ID from {os.path.basename(ATHLETE_FILE)}")
        if os.path.exists(ATHLETE_FILE):
            try:
                with open(ATHLETE_FILE, "r") as file:
                    data = json.load(file)
                    self.id = data.get("id")
                    logging.info(f"Athlete ID succesfully retrieved with the following id: {self.id}")
            except Exception as e:
                logging.error("Error loading token: %s", e)

        logging.info("Fetching Routes data")
        routes_url = f'https://www.strava.com/api/v3/athletes/{self.id}/routes'
        self.headers['page'] = str(page)
        self.headers['per_page'] = str(per_page)
        self.routes_data = self.make_request(routes_url, 'routes')
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

    async def fetch_and_save_routes_data_async(self) -> None:
        """
        Fetch and save Routes data asynchronously.

        :param data_type: Type of routes data to fetch 'routes'
        """
        start_time = time.time()
        logging.info(f"Starting asynchronous operation to fetch and save routes routes data")

        if self.routes_data:
            self.routes_ids_list = [route['id'] for route in self.routes_data]
            logging.info(f"Found {len(self.routes_ids_list)} routes in athlete data")
            logging.info(f"Starting asynchronous processing of routes routes")

            remaining_ids = self.routes_ids_list.copy()
            total_requests = len(remaining_ids)
            rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()

            logging.info(f"Rate limit status: {rate_limit_remaining} requests available out of {total_requests} needed")

            endpoint = {
                'routes': StravaEndpoints.ROUTES
            }['routes']

            while total_requests > rate_limit_remaining:
                start_while_time = time.time()
                logging.info(f"Rate limit reached: Processing {rate_limit_remaining} async requests (pending: {total_requests - rate_limit_remaining})")
                current_ids = remaining_ids[:rate_limit_remaining]
                await asyncio.gather(*(
                    self.process_endpoint(route_id, endpoint)
                    for route_id in current_ids
                ))
                logging.info(f"Async processing completed in {time.time() - start_while_time:.2f} seconds")

                current_time = time.localtime()
                wait_minutes = (15 - (current_time.tm_min % 15)) % 15
                wait_seconds = wait_minutes * 60 - current_time.tm_sec

                logging.warning(f"Waiting for {wait_minutes} minutes until next rate limit window")
                await asyncio.sleep(wait_seconds)

                remaining_ids = self.routes_ids_list[rate_limit_remaining:]
                total_requests = len(remaining_ids)
                self.make_readratelimit_api_call()
                rate_limit_remaining = RateLimitChecker(self.rate_limit_usage).get_rate_limit_remaining()
                logging.info(f"New rate limit status: {rate_limit_remaining} requests available")
                logging.info(f"Remaining requests to process: {total_requests}")

            else:
                start_else_time = time.time()
                logging.info(f"Processing {len(remaining_ids if remaining_ids else self.routes_ids_list)} async requests and save data operations")
                await asyncio.gather(*(
                    self.process_endpoint(route_id, endpoint)
                    for route_id in remaining_ids
                ))
                logging.info(f"Async processing completed in {time.time() - start_else_time:.2f} seconds")

        elif isinstance(self.routes_data, (list, dict)) and not self.routes_data:
            logging.warning(f"No routes routes data to process: Empty dataset received")
        else:
            logging.warning(f"Unable to process routes : No data available")

        logging.info(f"Total async processing time: {time.time() - start_time:.2f} seconds")