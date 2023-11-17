import requests
from pathlib import Path


def get_data(api_token: str):
    current_dir = Path(__file__).parent

    with open(current_dir / "get_data.graphql") as file:
        query = file.read()

    url = "https://api.github.com/graphql"
    json = {
        "query": query,
        "variables": {
            "login": "insolor"
        }
    }

    headers = {"Authorization": f"token {api_token}"}

    r = requests.post(url=url, json=json, headers=headers)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    from pprint import pprint
    from decouple import config
    token = config("GITHUB_TOKEN")
    pprint(get_data(token))
