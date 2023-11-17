import requests
import streamlit as st

headers = {
    # 'Accept': 'application/vnd.github+json',
    # 'Authorization': 'Bearer <YOUR-TOKEN>',
    # 'X-GitHub-Api-Version': '2022-11-28',
}

response = requests.get("https://api.github.com/users/insolor/orgs", headers=headers)
response.raise_for_status()

organizations = response.json()

data = []
markdown = ""

with st.spinner():
    for org in organizations:
        row = dict(
            image=org["avatar_url"],
            name=org["login"], 
            description=org["description"],
        )
        
        response = requests.get(org["url"])
        response.raise_for_status()
        org_info = response.json()
        
        row["url"] = org_info["html_url"]
        
        # data.append(row)
        markdown += f"""- <img src="{row["image"]}" width=24> [{row["name"]}]({row["url"]})\n"""

st.markdown(markdown, unsafe_allow_html=True)


# df = pd.DataFrame(data)

# st.data_editor(
#     df,
#     column_config={
#         "image": st.column_config.ImageColumn(),
#         "url": st.column_config.LinkColumn(),
#     }
# )
