from .utils import TokenManager, APIManager

def main():
    token_manager = TokenManager().get_token()
    access_token = token_manager["access_token"]

    client = APIManager(access_token)
    client.process_activities()

if __name__ == "__main__":
    main()