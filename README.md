# My Github Organizations

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://insolor-my-gh-orgs.streamlit.app)

Experimental streamlit dashboard to simplify working with multiple github organizations (e.g. quick access to their repos and issues).

Installation:
```
poetry install --no-root
```
Running:
```
poe run
```

## Configuration:

Secrets:
- `USER_LOGIN` - your user login
- `GITHUB_TOKEN` - your github personal access token, it can be generated here: https://github.com/settings/tokens

    At the moment a token for the application doesn't need any special rights, you can just generate a classic token with all cleared checkboxes.

## TODO:

- [x] get info about organizations and their repositories
- [x] show the info as markdown
- [x] show info about user's repos as a separate card
- [ ] sort repos by max(last_commit_datetime, update_datetime)
- [ ] show info in cards/tabs for each organization
- [ ] show info about all issues of an organization in a tab
