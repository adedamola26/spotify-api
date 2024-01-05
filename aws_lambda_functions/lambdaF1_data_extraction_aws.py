import json
import spotipy # added spotify layer for successful import
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import boto3
from datetime import datetime


def lambda_handler(event, context):
    # authenticate communication with spotify's servers
    auth_manager = SpotifyClientCredentials()

    # creating spotify object
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # top 100 songs url
    top_songs_playlist_url = 'https://open.spotify.com/playlist/5ABHKGoOzxkaa28ttQV9sE'

    # get top 100 songs id
    playlist_id = top_songs_playlist_url.split('/')[-1]

    # get the json file
    playlist_json = sp.playlist_tracks(playlist_id)

    client = boto3.client('s3')

    filename = f'spotify_raw_{str(datetime.now())}.json'

    client.put_object(
        Bucket='etl-project-spotify-api',
        Key=f'raw-data/to_be_processed/{filename}',
        Body=json.dumps(playlist_json)
    )