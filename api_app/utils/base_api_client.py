import aiohttp
import asyncio
import os
import json
import logging
from typing import Dict, Any, Optional

from .endpoint_config import EndpointConfig

import requests

class BaseAPIClient:
    ALLOWED_MODULES = ['athlete', 'activities', 'routes', 'clubs']

    def __init__(self, access_token: str):
        """
        Initialize the BaseAPIClient with an access token.

        :param access_token: The access token for authenticating API requests.
        """
        self.access_token = access_token
        self.headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.access_token}'
        }

    def make_request(self, url: str, module: str) -> Optional[Dict[str, Any]]:
        """
        Make a GET HTTPS request to the specified URL and return the JSON response.

        :param url: The URL to send the request to.
        :param module: The name of the module for logging purposes.
        :return: The JSON response as a dictionary, or None if an error occurs.
        """
        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        try:
            logging.info(f"Sending {module} request to %s", url)
            response = requests.get(url, headers=self.headers)
            self.rate_limit_usage = response.headers.get('x-readratelimit-usage')

            if response.status_code == 429:
                raise RateLimitExceededError()
            if response.status_code == 200:
                logging.info("Request successful")
                return response.json()
            else:
                logging.warning(f"Failed to fetch {module} data")
                logging.warning(f"Status: {response.status_code}")
                logging.warning(f"Reason: {response.reason}")
                return None
        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred: %s", http_err)
            return None
        except Exception as err:
            logging.error("An error occurred: %s", err)
            return None

    async def make_async_request(self, url: str, module: str) -> Optional[Dict[str, Any]]:
        """
        Make a asynchronous GET HTTPS request to the specified URL and return the JSON response.

        :param url: The URL to send the request to.
        :param module: The name of the module for logging purposes.
        :return: The JSON response as a dictionary, or None if an error occurs.
        """

        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        try:
            async with aiohttp.ClientSession() as session:

                rate_limit_checker = RateLimitChecker(self.rate_limit_usage)

                if not rate_limit_checker.can_proceed():
                    logging.warning("Rate limit exceeded. Cannot proceed with the request.")
                    return None

                async with session.get(url, headers=self.headers) as response:
                    logging.info(f"Sending {module} request to %s", url)
                    self.rate_limit_usage = response.headers.get('x-readratelimit-usage')
                    if response.status == 200:
                        return await response.json()
                    else:
                        logging.warning(f"Failed to fetch {module} data")
                        logging.warning(f"Status: {response.status}")
                        logging.warning(f"Reason: {response.reason}")
                        return None
        except Exception as e:
            logging.error(f"Error fetching {module} data: {str(e)}")
            return None

    def make_readratelimit_api_call(self):
        try:
            logging.info(f"Sending request to get read rate limit usage")
            response = requests.get('https://www.strava.com/api/v3/athlete', headers=self.headers)
            self.rate_limit_usage = response.headers.get('x-readratelimit-usage')

            if response.status_code == 200:
                logging.info("Request successful")
                return response.json()
            else:
                logging.warning("Failed to fetch read rate limit usage data")
                logging.warning(f"Status: {response.status_code}")
                logging.warning(f"Reason: {response.reason}")
                return None
        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred: %s", http_err)
            return None
        except Exception as err:
            logging.error("An error occurred: %s", err)
            return None

    async def check_json_file_exists(self, filename: str, module: str) -> bool:
        """
        Check if a JSON file already exists in the specified module directory.

        :param filename: The name of the file to check.
        :param module: The module name for validation against allowed modules.
        :return: True if the file exists, False otherwise.
        :raises ValueError: If the module is not allowed.
        """
        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        if module and module != 'athlete':
            data_dir = os.path.join(data_dir, module)

        file_path = os.path.join(data_dir, filename)
        exists = os.path.exists(file_path)

        if exists:
            logging.info(f"File {filename} already exists in {module} directory")

        return exists

    def save_json_to_file(self, data: dict, filename: str, module: str) -> None:
        """
        Save the given data to a JSON file.

        :param data: The data to save.
        :param filename: The name of the file to save the data to.
        :param module: The module name for validation against allowed modules.
        :raises ValueError: If the module is not allowed.
        """
        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        if module and module != 'athlete':
            data_dir = os.path.join(data_dir, module)

        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info("Data saved to %s", os.path.basename(file_path))

    async def save_json_to_file_async(self, data: dict, filename: str, module: str) -> None:
        """
        Save the given data to a JSON file.

        :param data: The data to save.
        :param filename: The name of the file to save the data to.
        :param module: The module name for validation against allowed modules.
        :raises ValueError: If the module is not allowed.
        """
        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        if module and module != 'athlete':
            data_dir = os.path.join(data_dir, module)

        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        async def _write_json():
            def write():
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
            await asyncio.to_thread(write)

        await _write_json()
        logging.info(f"Data saved asynchronously to {os.path.basename(file_path)}")

    async def process_endpoint(self, activity_id: int, endpoint_config: EndpointConfig):
        """
        Generic method to process an activity with a specific endpoint configuration.

        :param activity_id: The ID of the activity to process
        :param endpoint_config: The endpoint configuration to use
        :return: The processed activity data or None if an error occurs
        """
        filename = endpoint_config.filename_template(activity_id)
        section = endpoint_config.section
        try:
            url = endpoint_config.url_template(activity_id)
            logging.info(f"Processing {endpoint_config.endpoint_name} for activity {activity_id}")

            if await self.check_json_file_exists(filename, section):
                logging.info(f"Skipping {endpoint_config.endpoint_name} for activity {activity_id}: File exists")
                return None

            activity_data = await self.make_async_request(url, section)
            if activity_data:
                await self.save_json_to_file_async(activity_data, filename, section)
                return activity_data
            else:
                logging.warning(f"Unable to fetch {endpoint_config.endpoint_name} data for Activity ID {activity_id}")
                return None
        except Exception as e:
            logging.error(f"Error processing {endpoint_config.endpoint_name} for activity {activity_id}: {str(e)}")
            return None

class RateLimitChecker:
    def __init__(self, rate_limit_usage: Optional[str]):
        """
        Initialize the RateLimitChecker with the remaining rate limit.

        :param rate_limit_usage: The remaining rate limit value as a string.
        """
        self.rate_limit_remaining = int(100 - float(rate_limit_usage.replace(',', '.'))) if rate_limit_usage else 0

    def can_proceed(self) -> bool:
        """
        Check if the API calls can proceed based on the rate limit.

        :return: True if API calls can proceed, False otherwise.
        """
        return self.rate_limit_remaining > 0

    def get_rate_limit_remaining(self) -> int:
        """
        Check if the API calls can proceed based on the rate limit.

        :return: True if API calls can proceed, False otherwise.
        """
        return self.rate_limit_remaining

class RateLimitExceededError(SystemExit):
    """Exception raised when the API returns a 429 Too Many Requests status code.
    Inherits from SystemExit to stop the application."""
    def __init__(self, message="Rate limit exceeded: Too many requests. Application stopped."):
        self.message = message
        logging.critical(self.message)
        super().__init__()