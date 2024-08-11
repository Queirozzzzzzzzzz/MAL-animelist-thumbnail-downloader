import requests as req
import json
import os

directory_path = 'lists'
if not os.path.exists(directory_path):
            os.makedirs(directory_path)

def getUserAnimeList(clientId, username, limit):
    url = f'https://api.myanimelist.net/v2/users/{username}/animelist'
    res = req.get(url, params={'fields': 'list_status', 'limit': limit}, headers={
    'X-MAL-CLIENT-ID': clientId,
})

    if res.status_code == 200:
        data = res.json()

        # Save list as JSON
        file_name = '{}_animelist.json'.format(username)
        file_path = os.path.join(directory_path, file_name)

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        return f"Data saved successfully for user {username}."
    else:
        return f"Failed to fetch data. Status code: {res.status_code}"

