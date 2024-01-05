# ETL Pipeline For Creating Four 3NF Datasets Using Spotify API and AWS

## Executive Summary
I created four datasets (normalized to 3NF) based on a Spotify playlist containing the top 100 most streamed tracks. 

Although my goal in this project was to get acquainted with Amazon Web Services (AWS), the curated datasets can be used to explore a number of interests; for instance, as at 2nd of January, 2024: 

- Which artist(s) own the most number of tracks on the playlist?- _Post Malone_, _Ed Sheeran_ and _The Weeknd_ with 4 tracks each.

- Which artist performed in the most number of tracks on the playlist? - Post Malone, on 5 tracks 

- What's the percentage of tracks containing explicit content? - 31%

- How many albums featured the most tracks? - Olivia Rodrigo's _SOUR_, Ed Sheeran's _÷ (Deluxe)_ and _x (Deluxe Edition)_, Justin Bieber's _Purpose (Deluxe)_ and Imagine Dragon's _Evolve_, each with two entries
- etc.

## Methodology
Using Python as my programming language, I set my environment variables for SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET and extracted the playlist using Spotify's API. Then I parsed the JSON file to extract the data I deemed relevant for my desired datasets.

I performed the initial experiment in a Jupyter Notebook and migrated to AWS to implement the pipeline.

The following are the AWS-provided-services I employed as well as their reason for use:
- __AWS Lambda__
  
Used to host and run the source codes that performed the ETL. I created two Lambda functions; _first function_ for extracting the JSON file from the API and loading it in a specific directory in the project's S3 bucket and, the _other function_ for parsing the JSON file to four CSV files loaded into separate folders. 	

- __Amazon CloudWatch__
  
Used to schedule how often the First lambda function should run (set to every 1 hour for experimental purposes).

- __Amazon S3 (Simple Storage Service)__
  
Used to store all objects generated from different stages in the pipeline. Also used as a trigger for the second lambda function (i.e: when JSON file is loaded in a specified folder, begin transformation)

- __AWS Glue__
  
Used to crawl and catalog the data.

- __Amazon Athena__
  
Used to query and analyze the datasets.

## Architecture Diagram
The diagram below shows the architecture of the data pipeline. It was inspired by [Darshil Parmar](https://www.linkedin.com/in/darshil-parmar/).
![pipeline architecture](https://github.com/adedamola26/spotify-api/blob/main/architecture%20diagram.png)

## Final Dataset
The final datasets were normalized to the third normal form. The following is the Entity Relationship Diagram of showing the relationship between the four tables.

![ERD](https://github.com/adedamola26/spotify-api/blob/main/ERD.png)

__ALBUM__ _stores all albums with song entries on the playlist_
- album_id - an album's unique id (PK)
- album_name - the name of the album
- album_release_date - the date the album was released
- album_total_tracks - the number of tracks contained in the album
- album_owner_id - the unique id of the artist that owns tha album (FK)

__ARTIST__ _stores all artists that performed in at least one song on the playlist_
- artist_id - an artist's unique id (PK)
- artist_name - each artist's name

__TRACK__ _stores all tracks on the playlist_
- track_id - a track's unique id (PK)
- album_id - the unique id of the album that the track is contained in (FK)
- track_title - the title of the track
- track_number - the track's number in the album
- explicit - denotes whether the track contains explicit content (True) or not (False)
- duration_ms - the duration of the track in milliseconds
- rank - the track's rank on the leaderboard

__COLLABORATION__ _(the bridge that resolves the many-to-many relationship between ARTIST and TRACK)_
- track_id - the unique id of the track (PK,FK)
- artist_id - the unique id of the artist (PK,FK)

## Conclusion
I have explored various services provided by AWS to implement a pipeline that ETLs data from Spotify. This project allowed me to gain first-hand experience with AWS and I aim to expand on this experience in the near future.

