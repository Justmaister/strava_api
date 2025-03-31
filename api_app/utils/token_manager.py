import os
import sys
import time
import logging
import json
from typing import Optional

import requests
from dotenv import load_dotenv

from .thinker_pop_up import ask_for_code

load_dotenv()

TOKEN_FILE = "token_cache.json"

class TokenManager:
    API_URL = "https://www.strava.com/oauth/token"

    def __init__(self):
        """
        Initialize the TokenManager and load environment variables.
        """
        logging.info("Loading Environment Variables")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.refresh_token: Optional[str] = None
        self.access_token: Optional[str] = None
        self.expires_at: int = 0
        self.load_token()

    def load_token(self) -> None:
        """Load token from cache (file) if available."""
        logging.info(f"Loading Token from {TOKEN_FILE}")
        if os.path.exists(TOKEN_FILE):
            try:
                with open(TOKEN_FILE, "r") as file:
                    data = json.load(file)
                    self.access_token = data.get("access_token")
                    self.refresh_token = data.get("refresh_token")
                    self.expires_at = data.get("expires_at", 0)
            except Exception as e:
                logging.error("Error loading token: %s", e)

    def save_token(self, token_data: dict) -> None:
        """Save token to cache."""
        logging.info("Saving token to token_cache.json")
        try:
            with open(TOKEN_FILE, "w") as file:
                json.dump(token_data, file)
            logging.info("Token saved successfully.")
        except Exception as e:
            logging.error("Error saving token: %s", e)

    def is_token_valid(self) -> bool:
        """Check if the token is still valid.

        :return: True if the token is valid, False otherwise.
        """
        logging.info("Checking if the Tokens are still valid")
        if self.access_token and time.time() < self.expires_at:
            return True
        return False

    def get_token(self) -> dict:
        """Refresh token if expired.

        :return: The token data as a dictionary.
        """
        if self.is_token_valid():
            logging.info("Tokens are already valid")
            token_data = {
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "expires_at": self.expires_at
            }
            return token_data

        logging.info("The Tokens are not valid")
        self.code = ask_for_code()

        if self.code:
            logging.info(f"Sending response to {self.API_URL}")
            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": self.code,
                "grant_type": "authorization_code"
            }

            response = requests.post(self.API_URL, data=payload)
            response.raise_for_status()
            response_data = response.json()
            token_data = {
                "access_token": response_data.get("access_token", ""),
                "refresh_token": response_data.get("refresh_token", ""),
                "expires_at": response_data.get("expires_at", "")
            }

            self.save_token(token_data)
            return token_data

        else:
            logging.info("User did not enter any Strava Code. The application is shuting down. \n "
                         "For more details, visit: https://developers.strava.com/docs/getting-started/#oauth")
            sys.exit()

