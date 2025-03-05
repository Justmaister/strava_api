import os
from .utils.get_acces_token import APICache
from .utils.api_client import APIClient

def main():
    api_cache = APICache()
    data = api_cache.get_access_token()
    print("Data from API:", data)

    access_token = os.getenv('ACCESS_TOKEN')
    client = APIClient(access_token)

    athlete_data = client.get_athlete_data()
    if athlete_data:
        client.save_json_to_file(athlete_data, 'athlete_data.json')

    activities_data = client.get_activities_data(page=1, per_page=10)
    if activities_data:
        client.save_json_to_file(activities_data, 'activities_data.json')
        activity_ids = client.extract_activity_ids(activities_data)
        print("Activity IDs:", activity_ids)

if __name__ == "__main__":
    main()