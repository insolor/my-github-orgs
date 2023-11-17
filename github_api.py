from pathlib import Path

import requests

import streamlit as st

from models import ResponseModel


def get_data() -> ResponseModel:
    api_token = st.secrets["GITHUB_TOKEN"]
    
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
    return ResponseModel.model_validate(r.json())


if __name__ == "__main__":
    # Only for testing in dev environment
    import json

    from rich import print
    
    data = get_data()
    print(data)
