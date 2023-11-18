import pandas as pd
import streamlit as st

import github_api


user_data = github_api.get_data("insolor")


data = []
markdown = ""

with st.spinner():
    for org in user_data.organizations.nodes:
        
        row = dict(
            image=org.avatarUrl,
            name=org.name,
            description=org.description,
            url=org.url,
        )

        data.append(row)
        markdown += (
            f"""- <img src="{row["image"]}" width=16> [{row["name"]}]({row["url"]})\n"""
        )

st.markdown(markdown, unsafe_allow_html=True)

df = pd.DataFrame(data)

st.data_editor(
    df,
    column_config={
        "image": st.column_config.ImageColumn(),
        "url": st.column_config.LinkColumn(),
    }
)
