from dotenv import load_dotenv
import os
import base64
from requests import post,get
import json

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = CLIENT_ID + ':' + CLIENT_SECRET
    auth_byte = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_byte), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type" : "client_credentials"
    }

    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth(token):
    return {"Authorization" : "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)
    print(json_result)


def get_playlists(token):
    url = "https://api.spotify.com/v1/users/yourmum12505/playlists"
    headers = get_auth(token)
    query = "?offset=0&limit=50"

    result = get(url + query, headers=headers)
    json_result = json.loads(result.content)

    json_items = json_result["items"]
    #json_name = json_items["name"]

    names = [item['name'] for item in json_result['items']]

    print(names)


token = get_token()
#search_for_artist(token, "Drake")
get_playlists(token)

