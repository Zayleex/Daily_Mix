import requests, base64, random, config, json

client_id = config.client_id
client_secret = config.client_secret
concat_id_secret = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()


def get_rndm_num(song_count, playlist_length):
    rndm_num_array = []
    while len(rndm_num_array) < song_count:
        ran_num = random.randint(0, playlist_length - 1)
        if ran_num in rndm_num_array:
            continue
        else:
            rndm_num_array.append(ran_num)
    return rndm_num_array


def get_playlist_items():
    playlist_id = config.playlist_source
    inital_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    array_id = []
    header = {
        "Authorization": "Bearer " + refresh_token()
    }
    inital_response = requests.get(url=inital_url, headers=header).json()
    for i in range(len(inital_response["tracks"]["items"])):
        array_id.append(inital_response["tracks"]["items"][i]["track"]["id"])
    new_url = inital_response["tracks"]["next"]
    while new_url is not None:
        response = requests.get(url=new_url, headers=header).json()
        for e in range(len(response["items"])):
            array_id.append(response["items"][e]["track"]["id"])
        new_url = response["next"]
    song_pos = get_rndm_num(100, int(inital_response["tracks"]["total"]))
    song_id_array = []
    for x in song_pos:
        song_id = array_id[x]
        song_id_array.append(f"spotify:track:{song_id}")
    add_songs_playlist(song_id_array)


def add_songs_playlist(song_id_array):
    playlist_id = config.playlist_destination
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    header = {
        "Authorization": "Bearer " + refresh_token(),
        "Content-Type": "application/json"
    }
    data = {
        "uris": song_id_array,
        "position": 0
    }
    request = requests.post(url=url, headers=header, data=json.dumps(data))


def refresh_token():
    refresh_token = config.refresh_token
    url = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization": "Basic " + concat_id_secret,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }
    response = requests.post(url=url, headers=header, data=data).json()["access_token"]
    return response

