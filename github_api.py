from pathlib import Path

import requests
import streamlit as st

from models import Error, ResponseModel, User


def get_data(login: str) -> tuple[User, list[Error] | None]:
    api_token = st.secrets["GITHUB_TOKEN"]

    current_dir = Path(__file__).parent

    with open(current_dir / "get_data.graphql") as file:
        query = file.read()

    url = "https://api.github.com/graphql"
    request_params = dict(
        query=query,
        variables=dict(login=login),
    )

    headers = dict(Authorization="token " + api_token)

    response = requests.post(url=url, json=request_params, headers=headers)
    response.raise_for_status()

    model = ResponseModel.model_validate(response.json())
    return model.data.user if model.data else None, model.errors


if __name__ == "__main__":
    # Only for testing in dev environment
    from rich import print

    data, errors = get_data("insolor")
    print(data)
    print(errors)
