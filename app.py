import io

import pandas as pd
import streamlit as st

import github_api

with st.spinner("Getting data..."):
    user_data = github_api.get_data("insolor")


markdown = io.StringIO()

for org in user_data.organizations.nodes:
    print(f"""## <img src="{org.avatarUrl}" width=24> [{org.name}]({org.url})""", file=markdown)
    
    if org.description:
        print(org.description, end="\n\n", file=markdown)
    
    if org.repositories.nodes:
        print("### Repositories", file=markdown)
        
        for repo in org.repositories.nodes:
            if repo.description:
                print(f"- [{repo.name}]({repo.url}): {repo.description}", file=markdown)
            else:
                print(f"- [{repo.name}]({repo.url})", file=markdown)

st.markdown(markdown.getvalue(), unsafe_allow_html=True)
