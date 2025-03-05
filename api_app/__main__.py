import os
from .utils.get_acces_token import APICache
from .utils.api_client import APIClient

def main():
    api_cache = APICache()
    data = api_cache.get_access_token()

    # access_token = data['access_token']
    access_token = os.getenv('ACCESS_TOKEN') # For developing purpouses
    client = APIClient(access_token)

    client.fetch_and_save_athlete_data()
    client.fetch_and_save_athlete_activities_data(page=1, per_page=10)
    client.fetch_and_save_activities_data()

if __name__ == "__main__":
    main()