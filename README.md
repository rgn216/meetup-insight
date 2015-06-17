#My project at Insight Data Engineering : Uncovering meetup.com's social network

meetup.com is a great social networking portal : after subscribing to meetup groups, each user receives recommendations for events where he can meet like-minded people.
How about having a recommender system based on similarities rather than user defined activity preferences ?

## Data Pipeline

To be completed

## Data Collection

I wrote Python scripts to collect the data made accessible through meetup.com's API. The data, available in JSON format falls into different categories : groups, events, members, and RSVP (streaming API). For the purpose of this project, I limited my focus to San Francisco data.

## Data transformation

The JSON files are then parsed, converted into csv files and stored in HDFS (Source of Truth)

## Batch processing

The batch processing is then performed in Hive, resulting in two weighted graphs representing the degree of similarity between two users :
- number of events attended by the two users
- number of topics of interest in common

## User interface


## Interesting statistics


## Next steps

If I had more time I would have liked to streamline the data ingestion using Kafka technology to append RSVP data in real time