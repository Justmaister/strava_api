from .utils.get_acces_token import APICache

def main():
    api_cache = APICache()
    data = api_cache.get_access_token()
    print("Data from API:", data)

if __name__ == "__main__":
    main()