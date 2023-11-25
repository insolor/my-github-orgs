import io
from contextlib import redirect_stdout
from datetime import timedelta

import streamlit as st

import github_api
from models import OrganizationNode, User

st.set_page_config(page_title="My Github Organizations")


@st.cache_data(show_spinner="Getting data...", ttl=timedelta(minutes=30))
def get_data(login: str) -> User:
    return github_api.get_data(login)


user_data = get_data("insolor")

nodes = user_data.organizations.nodes.copy()
nodes.insert(0, user_data)

with redirect_stdout(io.StringIO()) as markdown:
    for item in nodes:
        if isinstance(item, OrganizationNode) and item.description:
            print(f"""### <img src="{item.avatarUrl}" width=24> [{item}]({item.url} "{item.description}")""")
        else:
            print(f"""### <img src="{item.avatarUrl}" width=24> [{item}]({item.url})""")

        if item.repositories.nodes:
            for repo in item.repositories.nodes:
                if repo.description:
                    print(f"""- [{repo.name}]({repo.url} "{repo.description}")""")
                else:
                    print(f"- [{repo.name}]({repo.url})")

st.markdown(markdown.getvalue(), unsafe_allow_html=True)
