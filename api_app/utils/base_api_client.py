import os
import json
import logging
import requests
from typing import Dict, Any, Optional

class BaseAPIClient:
    ALLOWED_MODULES = ['activities', 'routes']  # Define allowed modules for saving data

    def __init__(self, access_token: str):
        """
        Initialize the BaseAPIClient with an access token.

        :param access_token: The access token for authenticating API requests.
        """
        self.access_token = access_token
        self.headers = {
            'accept': 'application/json',  # Specify that we want JSON responses
            'authorization': f'Bearer {self.access_token}'  # Set the authorization header
        }

    def make_request(self, url: str, module: str) -> Optional[Dict[str, Any]]:
        """
        Make a GET request to the specified URL and return the JSON response.

        :param url: The URL to send the request to.
        :param module: The name of the module for logging purposes.
        :return: The JSON response as a dictionary, or None if an error occurs.
        """
        try:
            logging.info(f"Sending {module} request to %s", url)
            response = requests.get(url, headers=self.headers)  # Send the GET request
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            logging.info("Request successful")
            return response.json()  # Return the JSON response
        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred: %s", http_err)
            return None
        except Exception as err:
            logging.error("An error occurred: %s", err)
            return None

    def save_json_to_file(self, data: dict, filename: str, module: str = '') -> None:
        """
        Save the given data to a JSON file.

        :param data: The data to save.
        :param filename: The name of the file to save the data to.
        :param module: The module name for validation against allowed modules.
        :raises ValueError: If the module is not allowed.
        """
        # Validate the module name if provided
        if module and module not in self.ALLOWED_MODULES:
            raise ValueError(f"Invalid module: {module}. Allowed modules are: {', '.join(self.ALLOWED_MODULES)}")

        # Define the directory to save the data
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        if module:
            data_dir = os.path.join(data_dir, module)
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)

        # Write the data to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info("Data saved to %s", file_path)
