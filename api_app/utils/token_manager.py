import os
import requests
import webbrowser
import sys
import time
import logging
import json
import threading
from typing import Optional
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv

load_dotenv()

AUTH_CODE = None
REDIRECT_PORT = 8000
SERVER_HOST = 'localhost'
API_URL = "https://www.strava.com/oauth/token"
TOKEN_FILE = "token_cache.json"


class StravaAuthHandler(BaseHTTPRequestHandler):
    """A simple handler to capture the authorization code from the redirect URL."""
    def do_GET(self):
        global AUTH_CODE
        query_components = parse_qs(urlparse(self.path).query)

        if 'code' in query_components:
            AUTH_CODE = query_components['code'][0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization successful!</h1><p>You can now close or minimise this browser window and return to the application.</p></body></html>")

            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error: Code not found in redirect.")

class TokenManager():
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

        client_id = self.client_id
        client_secret = self.client_secret
        global REDIRECT_PORT

        redirect_uri = f'http://{SERVER_HOST}:{REDIRECT_PORT}'

        request_url = (
            f'http://www.strava.com/oauth/authorize?client_id={client_id}'
            f'&response_type=code&redirect_uri={redirect_uri}'
            f'&approval_prompt=force'
            f'&scope=profile:read_all,activity:read_all'
        )

        logging.info("Opening browser for Strava authorization...")
        webbrowser.open(request_url)

        httpd = HTTPServer((SERVER_HOST, REDIRECT_PORT), StravaAuthHandler)
        logging.info(f"Waiting for Strava authorization on {redirect_uri}...")

        httpd.serve_forever()
        logging.info("Server shut down. Continuing script...")

        code = AUTH_CODE

        if not code:
            logging.info("Authorization failed or code was not received.")
            return None

        token = requests.post(
            url='https://www.strava.com/api/v3/oauth/token',
            data={'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'grant_type': 'authorization_code'}
        )
        token_json = token.json()

        self.save_token(token_json)
        return token_json

