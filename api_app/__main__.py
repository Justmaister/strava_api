import os
from .utils.get_acces_token import APICache
from .utils.api_client import APIClient

def main():
    api_cache = APICache()
    data = api_cache.get_access_token()
    print("Data from API:", data)

    access_token = os.getenv('ACCESS_TOKEN')
    client = APIClient(access_token)

    client.fetch_and_save_athlete_data()
    client.fetch_and_save_activities_data(page=1, per_page=10)

if __name__ == "__main__":
    main()