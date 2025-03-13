from .utils import APIClient, TokenManager

def main():
    token_manager = TokenManager().get_token()
    access_token = token_manager["access_token"]

    client = APIClient(access_token)
    client.process_activities()

if __name__ == "__main__":
    main()