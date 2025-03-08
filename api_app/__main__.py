import os
# from .utils.get_acces_token import APICache
from .utils.api_client import APIClient
from .utils.token_manager import TokenManager

def main():
    # api_cache = APICache()
    # data = api_cache.get_access_token()
    # access_token = data['access_token']
    # access_token = os.getenv('ACCESS_TOKEN') # For developing purpouses

    token_manager = TokenManager().get_token()
    access_token = token_manager["access_token"]


    client = APIClient(access_token)
    client.process_activities()

if __name__ == "__main__":
    main()