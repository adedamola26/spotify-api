import json
import boto3
from datetime import datetime
import pandas as pd # added pandas layer for successful import
from io import StringIO


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = 'etl-project-spotify-api'
    Key = 'raw-data/to_be_processed/'

    def collect_albums(data):
        album_list = []

        # assuming an album is owned by only one artist
        for i in range(100):
            album = data['items'][i]['track']['album']

            album_id = album['id']
            album_name = album['name']
            album_type = album['type']
            album_release_date = album['release_date']
            album_total_tracks = album['total_tracks']
            album_owner_id = album['artists'][0]['id']
            album_owner_name = album['artists'][0]['name']

            album_list.append(
                {
                    'album_id': album_id,
                    'album_name': album_name,
                    'album_release_date': album_release_date,
                    'album_total_tracks': album_total_tracks,
                    'album_type': album_type,
                    'album_owner_id': album_owner_id,
                    'album_owner_name': album_owner_name
                }
            )
        return album_list

    def collect_artists(data):
        artist_list = []

        for i in range(100):  # playlist will always contain 100 songs
            artists = data['items'][i]['track']['artists']

            for artist in artists:  # considering collaborations
                artist_id = artist['id']
                artist_name = artist['name']
                artist_type = artist['type']

                artist_list.append(
                    {
                        'artist_id': artist_id,
                        'artist_name': artist_name,
                        'artist_type': artist_type
                    }
                )
        return artist_list

    def collect_tracks(data):
        # tracks
        track_list = []
        for i in range(100):
            track = data['items'][i]['track']
            album_id = data['items'][i]['track']['album']['id']

            track_id = track['id']
            track_title = track['name']
            track_number = track['track_number']
            track_type = track['type']
            explicit = track['explicit']
            duration_ms = track['duration_ms']
            rank = i + 1

            track_list.append(
                {
                    'track_id': track_id,
                    'album_id': album_id,
                    'track_title': track_title,
                    'track_number': track_number,
                    'track_type': track_type,
                    'explicit': explicit,
                    'duration_ms': duration_ms,
                    'rank': rank
                }
            )
        return track_list

    def collect_collabs(data):
        collaboration_list = []

        for i in range(100):
            track = data['items'][i]['track']

            track_id = track['id']
            artists = track['artists']

            for artist in artists:
                collaboration_list.append(
                    {
                        'track_id': track_id,
                        'artist_id': artist['id']
                    }
                )
        return collaboration_list

    spotify_data = []
    spotify_keys = []

    for content in s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents']:
        if content['Key'][-5:] == '.json':
            file = content['Key']
            response = s3.get_object(
                Bucket=Bucket,
                Key=file
            )
            content = response['Body']
            jsonObject = json.loads(content.read())

            spotify_data.append(jsonObject)
            spotify_keys.append(file)

    for data in spotify_data:
        albums_data = collect_albums(data)
        artists_data = collect_artists(data)
        collabs_data = collect_collabs(data)
        tracks_data = collect_tracks(data)

        album_df = pd.DataFrame(albums_data)
        artist_df = pd.DataFrame(artists_data)
        track_df = pd.DataFrame(tracks_data)
        collab_df = pd.DataFrame(collabs_data)

        new_artist = {
            'artist_id': '0LyfQWJT6nXafLPZqxe9Of',
            'artist_name': 'Various Artists'
        }

        artist_df = pd.concat([artist_df, pd.DataFrame([new_artist])], ignore_index=True)

        album_df = album_df.drop(['album_owner_name'], axis=1)
        album_df.head()
        album_df = album_df.drop(['album_type'], axis=1)
        artist_df = artist_df.drop(['artist_type'], axis=1)
        track_df = track_df.drop(['track_type'], axis=1)

        album_df = album_df.drop_duplicates().reset_index(drop=True)
        artist_df = artist_df.drop_duplicates().reset_index(drop=True)

        track_key = f'transformed-data/track-data/transformed_track_{datetime.now()}.csv'
        track_buffer = StringIO()
        track_df.to_csv(track_buffer, index=False)
        track_content = track_buffer.getvalue()
        s3.put_object(
            Bucket='etl-project-spotify-api',
            Key=track_key,
            Body=track_content
        )

        album_key = f'transformed-data/album-data/transformed_album_{datetime.now()}.csv'
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index=False)
        album_content = album_buffer.getvalue()
        s3.put_object(
            Bucket='etl-project-spotify-api',
            Key=album_key,
            Body=album_content
        )

        artist_key = f'transformed-data/artist-data/transformed_artist_{datetime.now()}.csv'
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(
            Bucket='etl-project-spotify-api',
            Key=artist_key,
            Body=artist_content
        )

        collab_key = f'transformed-data/collab-data/transformed_collab_{datetime.now()}.csv'
        collab_buffer = StringIO()
        collab_df.to_csv(collab_buffer, index=False)
        collab_content = collab_buffer.getvalue()
        s3.put_object(
            Bucket='etl-project-spotify-api',
            Key=collab_key,
            Body=collab_content
        )
    s3_resource = boto3.resource('s3')

    for key in spotify_keys:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(
            copy_source,
            Bucket,
            f'raw-data/processed/{key.split("/")[-1]}'
        )
        s3_resource.Object(Bucket, key).delete()