Executive Summary
I created four datasets (normalized to 3NF) based off of a Spotify playlist containing the top 100 most streamed tracks. 

My aim in this project was to get acquainted with AWS. Regardless, the curated dataset could be used to explore a number of interests; for instance, as at 2nd of January, 2024: 

- Which artist(s) own the most number of tracks in the playlist?- Post Malone, Ed Sheeran and The Weeknd with 4 tracks each.

- Which artist performed in the most number of tracks on the playlist? -Post Malone, 5 times 

- What's the percentage of tracks containing explicit content? (31%)

- How many albums featured the most tracks? 
Olivia Rodrigo's SOUR, Ed Sheeran's ÷ (Deluxe) and x (Deluxe Edition), Justin Bieber's Purpose (Deluxe) and Imagine Dragon's Evolve, each with two entries.

Project inspired by Darshil

Here's the link to the project and other necessary details

By the way, I wish you a lovely year ahead.

Methodology
After setting my environment variables for SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET, I extracted the playlist using Spotify's API. Then I parsed the '.json' to extract the data I deemed relevant for my desired datasets. Here and the names given to my final datasets (in my Jupyter Notebook) along with their purpose.

album_df - stores all albums with song entries on the playlist
track_df - stores all tracks on the playlist
artist_df - stores all artists that performed in at least one song on the playlist
collab_df - resolves the many-to-many relationship between artists and songs.

I performed the initial experiment in a Jupyter Notebook and when I was satisfied with my results, I migrated to Amazon Web Services (AWS) to implement the pipeline.

The following are the AWS tools I employed for the following reasons:, I used: Amazon Cloud Watch, Amazon Lambda, Amazon S3, Amazon Glue, Amazon Athena, Trigger functions.

Amazon Lambda
---- Used to host and run the source codes that performed the ETL. I created two Lambda functions; one function for extracting the .json file from the API and loading it in a specific directory in the project's S3 bucket and, the other function for parsing the .json file to four '.csv' files loaded into separat directories. 	

- Amazon Cloud Watch
---- Used to schedule how often the First lambda function should run (set to every 1 hour for experiment purposes).

Amazon S3 (Simple Storage Service) 
---- Used to store all objects generated from different stages in the pipeline. Also used as a trigger for the second lambda function (i.e: when .json file is loaded in X folder, begin transfromation) With it I stored the '.json' file that the API returned on every call, the final datasets in '.csv' format and my query resulsts from Amazon Athena.

- Amazon Glue
---- Used to clean and prepare my data for analysis.

- Amazon Athena
---- Used to query and analyse the datasets.


The final datasets were normalized to the third normal form. Listed below are the columns contained in each dataset:
(PK means Primary Key, FK means Foreign Key)
album_df
- album_id - an album's unique id (PK)
- album_name - the name of the album
- album_release_date - the date the album was released
- album_total_tracks - the number of tracks contained in the album
- album_owner_id - the unique id of the artist that owns tha album (FK)

artist_df
- artist_id - an artist's unique id (PK)
- artist_name - each artist's name

track_df
- track_id - a track's unique id (PK)
- album_id - the unique id of the album that the track is contained in (FK)
- track_title - the title of the track
- track_number - the track's number in the album
- explicit - denotes whether the track contains explicit content (True) or not (False)
- duration_ms - the duration of the track in milliseconds
- rank - the track's rank on the leaderboard

collab_df (the bridge dataset between artist_df and track_df)
- track_id - the unique id of the track (PK,FK)
- artist_id - the unique id of the artist (PK,FK)

Conclusion
I have explored various services provided by AWS to implement a pipeline that ETLs data from Spotify. This project allowed me to gain first-hand experience with AWS and I aim to expand on this experience in the near future.

