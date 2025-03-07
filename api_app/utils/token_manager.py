import requests
import json
import os
import time
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

TOKEN_FILE = "token_cache.json"

class TokenManager:
    API_URL = "https://www.strava.com/oauth/token"


    def __init__(self):
        logging.info("Loading Environment Variables")
        ## Cambiar el code per executarse al inicial la applicacio
        self.code = os.getenv("CODE")

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.refresh_token = None
        self.token = None
        self.expires_at = 0
        self.load_token()

    def load_token(self):
        """Load token from cache (file) if available."""
        logging.info("Loading Token from token_cache.json")
        if os.path.exists(TOKEN_FILE):
            logging.info("I am here")
            try:
                with open(TOKEN_FILE, "r") as file:
                    data = json.load(file)
                    self.token = data.get("access_token")
                    self.refresh_token = data.get("refresh_token")
                    self.expires_at = data.get("expires_at", 0)
            except Exception as e:
                logging.error("Error loading token: %s", e)

    def save_token(self, token_data):
        """Save token to cache."""
        logging.info("Saving token to token_cache.json")
        with open(TOKEN_FILE, "w") as file:
            json.dump(token_data, file)

    def is_token_valid(self):
        """Check if the token is still valid."""
        logging.info("Checking if the Tokens are still valid")
        if not self.token and time.time() < self.expires_at:
            return True
        # else:
        #     return None

    def get_token(self):
        """Refresh token if expired."""
        if self.is_token_valid():
            logging.info("Tokens are already valid")
            return

        logging.info("The Tokens are not valid")
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
        logging.info(f'the token data: {token_data}')
        self.save_token(token_data)
        # self._update_token(token_data)

    def _update_token(self, token_data):
        """Update the token and cache it."""
        self.token = token_data["access_token"]
        self.refresh_token = token_data["refresh_token"]
        self.expires_at = token_data["expires_at"]
        self.save_token(token_data)



if __name__ == "__main__":
    token_manager = TokenManager()
    data = token_manager.get_token()
    print(data)
