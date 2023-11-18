from datetime import timedelta
import io
from contextlib import redirect_stdout

import streamlit as st

import github_api

st.set_page_config(page_title="My Github Organizations")


@st.cache_data(show_spinner="Getting data...", ttl=timedelta(minutes=30))
def get_data(login: str):
    return github_api.get_data(login)


user_data = get_data("insolor")

with redirect_stdout(io.StringIO()) as markdown:
    for org in user_data.organizations.nodes:
        if org.description:
            print(f"""### <img src="{org.avatarUrl}" width=24> [{org.name}]({org.url} "{org.description}")""")
        else:
            print(f"""### <img src="{org.avatarUrl}" width=24> [{org.name}]({org.url})""")

        if org.repositories.nodes:
            for repo in org.repositories.nodes:
                if repo.description:
                    print(f"""- [{repo.name}]({repo.url} "{repo.description}")""")
                else:
                    print(f"- [{repo.name}]({repo.url})")

st.markdown(markdown.getvalue(), unsafe_allow_html=True)
