import requests
from environs import Env

env = Env()
env.read_env()

# Define your applicaion 's Client ID and Client Secret
def getAcessToken():
    clientId = env('CLIENT_ID')
    clientSecret = env('CLIENT_SECRET')
    tokenURL = "https://api.intra.42.fr/oauth/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": clientId,
        "client_secret": clientSecret
    }

    # Make a POST request to obtain the access token
    response = requests.post(tokenURL, data=data)
    # Check if the request was successful
    if response.status_code == 200:
        access_token = response.json()
        return access_token
    else:
        raise ValueError("Failed to obtain access token")

print(getAcessToken())
