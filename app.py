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


user_data, errors = get_data(st.secrets["USER_LOGIN"])

if errors:
    for error in errors:
        st.error(error)

if user_data:
    nodes = user_data.organizations.nodes.copy()
    nodes.insert(0, user_data)

    names_map = {str(node.login): node for node in nodes}

    selected = option_menu(None, list(names_map.keys()), menu_icon="cast", default_index=0, orientation="vertical")

    if selected:
        user_or_org = names_map[selected]
        with st.empty():
            with redirect_stdout(io.StringIO()) as markdown:
                if isinstance(user_or_org, OrganizationNode) and user_or_org.name:
                    print(f"""### <img src="{user_or_org.avatarUrl}" width=24> [{user_or_org.login}]({user_or_org.url} "{user_or_org.name}")""")
                else:
                    print(f"""### <img src="{user_or_org.avatarUrl}" width=24> [{user_or_org.login}]({user_or_org.url})""")

                for repo in user_or_org.repositories.nodes:
                    owner = repo.owner
                    if owner and owner.login != user_or_org.login and owner.login in names_map:
                        continue
                    
                    own_repository = repo.owner is None or repo.owner.login == user_or_org.login
                    repo_name = repo.name if own_repository else repo.nameWithOwner
                    
                    if repo.description:
                        description = repo.description.replace('"', r"\"")
                        print(f"""- [{repo_name}]({repo.url} "{description}")""", end="")
                    else:
                        print(f"- [{repo_name}]({repo.url})", end="")

                    if repo.stargazerCount:
                        print(f" ☆{repo.stargazerCount}", end="")

                    if not own_repository:
                        print(" (outside collaborator)", end="")
                    elif repo.parent:
                        parent = repo.parent
                        print(f" (fork of [{parent.nameWithOwner}]({parent.url}))", end="")

                    print()

            st.markdown(markdown.getvalue(), unsafe_allow_html=True)
