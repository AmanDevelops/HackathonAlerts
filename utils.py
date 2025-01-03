import requests
import json


import requests

uuid = "YOUR_UNIQUE_ID"

response = requests.get(f'https://devfolio.co/_next/data/{uuid}/hackathons.json')

data = response.json()

print(json.dumps(data['pageProps']['dehydratedState']['queries'][0]['state']['data']['open_hackathons'][2], indent=4))
