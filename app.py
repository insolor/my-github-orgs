import io
from contextlib import redirect_stdout
from datetime import timedelta

import streamlit as st
from streamlit_option_menu import option_menu

import github_api
from models import Error, OrganizationNode, User

st.set_page_config(page_title="My Github Organizations")


@st.cache_data(show_spinner="Getting data...", ttl=timedelta(minutes=30))
def get_data(login: str) -> tuple[User, list[Error] | None]:
    return github_api.get_data(login)


user_data, errors = get_data("insolor")

if errors:
    for error in errors:
        st.error(error)

if user_data:
    nodes = user_data.organizations.nodes.copy()
    nodes.insert(0, user_data)

    names_map = {str(node.login): node for node in nodes}

    selected = option_menu(None, list(names_map.keys()), menu_icon="cast", default_index=0, orientation="vertical")

    if selected:
        item = names_map[selected]
        with st.empty():
            with redirect_stdout(io.StringIO()) as markdown:
                if isinstance(item, OrganizationNode) and item.name:
                    print(f"""### <img src="{item.avatarUrl}" width=24> [{item.login}]({item.url} "{item.name}")""")
                else:
                    print(f"""### <img src="{item.avatarUrl}" width=24> [{item.login}]({item.url})""")

                for repo in item.repositories.nodes:
                    if repo.description:
                        description = repo.description.replace('"', r"\"")
                        print(f"""- [{repo.name}]({repo.url} "{description}")""", end="")
                    else:
                        print(f"- [{repo.name}]({repo.url})", end="")

                    if repo.stargazerCount:
                        print(f" ☆{repo.stargazerCount}", end="")

                    if repo.parent:
                        parent = repo.parent
                        print(f" (fork of [{parent.nameWithOwner}]({parent.url}))", end="")

                    print()

            st.markdown(markdown.getvalue(), unsafe_allow_html=True)
