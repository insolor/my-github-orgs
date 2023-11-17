from pathlib import Path

import requests

from models import ResponseModel


def get_data(api_token: str) -> ResponseModel:
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

    headers = {"Authorization": "token " + api_token}

    r = requests.post(url=url, json=json, headers=headers)
    r.raise_for_status()
    return ResponseModel.parse_obj(r.json())


if __name__ == "__main__":
    # Only for testing in dev environment
    import json

    from decouple import config
    from rich import print
    
    token = config("GITHUB_TOKEN")
    data = get_data(token)
    print(data)
