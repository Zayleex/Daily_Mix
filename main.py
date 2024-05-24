import requests
import base64
import random
import config
import json

client_id = config.client_id
client_secret = config.client_secret
concat_id_secret = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()


def get_playlist_tracks(playlist_id):
    initial_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    playlist_tracks = []
    header = {
        "Authorization": "Bearer " + get_refresh_token()
    }
    initial_response = requests.get(url=initial_url, headers=header).json()
    for initial_tracks in range(len(initial_response["tracks"]["items"])):
        playlist_tracks.append(f"spotify:track:{initial_response["tracks"]["items"][initial_tracks]["track"]["id"]}")
    new_url = initial_response["tracks"]["next"]
    while new_url is not None:
        response = requests.get(url=new_url, headers=header).json()
        for tracks in range(len(response["items"])):
            playlist_tracks.append(f"spotify:track:{response["items"][tracks]["track"]["id"]}")
        new_url = response["next"]
    return playlist_tracks


def get_random_tracks(playlist_tracks):
    track_position = get_random_numbers(100, int(len(playlist_tracks)))
    new_playlist_array = []
    for position in track_position:
        track_id = playlist_tracks[position]
        new_playlist_array.append(track_id)
    add_songs_playlist(new_playlist_array)


def get_random_numbers(song_count, playlist_length):
    random_numbers_array = []
    while len(random_numbers_array) < song_count:
        ran_num = random.randint(0, playlist_length - 1)
        if ran_num in random_numbers_array:
            continue
        else:
            random_numbers_array.append(ran_num)
    return random_numbers_array


def add_songs_playlist(song_id_array):
    playlist_id = config.playlist_destination.split("?")[0]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    header = {
        "Authorization": "Bearer " + get_refresh_token(),
        "Content-Type": "application/json"
    }
    data = {
        "uris": song_id_array,
        "position": 0
    }
    requests.post(url=url, headers=header, data=json.dumps(data))


def remove_songs_playlist(playlist_tracks):
    playlist_id = config.playlist_destination.split("?")[0]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    header = {
        "Authorization": "Bearer " + get_refresh_token(),
        "Content-Type": "application/json"
    }
    data = {
        "tracks": [{"uri": uri} for uri in playlist_tracks],
    }
    requests.delete(url=url, headers=header, data=json.dumps(data))


def get_refresh_token():
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


remove_songs_playlist(get_playlist_tracks(config.playlist_destination))
get_random_tracks(get_playlist_tracks(config.playlist_source))
