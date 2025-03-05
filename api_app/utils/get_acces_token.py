# Implementa el patrón Singleton, asegurando que solo haya una instancia de APICache.
# Usa __new__ para garantizar que solo se crea una instancia única.


import requests
import json
import logging
import os
from typing import Any, Dict
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv('.env')

class APICache:
    _instance = None
    _data = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APICache, cls).__new__(cls)
        return cls._instance

    def get_access_token(self) -> Dict[str, Any]:
        if self._data is None:
            self._make_api_call()
        return self._data

    def _make_api_call(self) -> Dict[str, Any]:
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        code = os.getenv('CODE')
        code = 'f8cae06dd860972bfa9acfecdf8b7c192555ff3d'
        url = f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code"

        try:
            payload = {}
            headers = {}

            logging.info("Sending Token request")
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            self._data = json.loads(response.text)
            logging.info("Request successful: %s", self._data)

        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred: %s", http_err)
        except Exception as err:
            logging.error("An error occurred: %s", err)
