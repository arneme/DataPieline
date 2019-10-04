class SparkifySqlQueries:

  # DROP TABLES

  staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
  staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
  songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
  user_table_drop = "DROP TABLE IF EXISTS user_table"
  song_table_drop = "DROP TABLE IF EXISTS song_table"
  artist_table_drop = "DROP TABLE IF EXISTS artist_table"
  time_table_drop = "DROP TABLE IF EXISTS time_table"

  # CREATE TABLES

  # First, define the staging tables. These tables will just mirror the
  # input data from the events and song data csv files

  staging_events_table_create = ("""
  CREATE TABLE IF NOT EXISTS staging_events (
    event_id BIGINT IDENTITY(0,1) NOT NULL,
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender VARCHAR,
    itemInSession BIGINT,
    lastName VARCHAR,
    length DECIMAL(10,5),
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration VARCHAR,
    sessionId INTEGER NOT NULL SORTKEY DISTKEY,
    song VARCHAR,
    status INTEGER,
    ts BIGINT,
    userAgent VARCHAR,
    userId INTEGER
  );
  """)

  staging_songs_table_create = ("""
  CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INTEGER NOT NULL,
    artist_id VARCHAR NOT NULL SORTKEY DISTKEY,
    artist_latitude DECIMAL(9,5),
    artist_longitude DECIMAL(9,5),
    artist_location VARCHAR,
    artist_name VARCHAR NOT NULL,
    song_id VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    duration DECIMAL(10,5),
    year INTEGER NOT NULL
  );
  """)

  # Create the dimension tables

  songplay_table_create = ("""
  CREATE TABLE IF NOT EXISTS songplay_table(
     songplay_id INTEGER IDENTITY(0,1) NOT NULL SORTKEY,
     start_time TIMESTAMP NOT NULL,
     user_id VARCHAR NOT NULL DISTKEY,
     song_id VARCHAR NOT NULL,
     artist_id VARCHAR NOT NULL,
     level VARCHAR NOT NULL,
     session_id INT NOT NULL,
     location VARCHAR,
     user_agent VARCHAR
  );
  """)


  user_table_create = ("""
  CREATE TABLE IF NOT EXISTS user_table(
     user_id VARCHAR NOT NULL SORTKEY,
     first_name VARCHAR NOT NULL,
     last_name VARCHAR NOT NULL,
     gender VARCHAR NOT NULL,
     level VARCHAR NOT NULL
  );
  """)

  song_table_create = ("""
  CREATE TABLE IF NOT EXISTS song_table(
     song_id VARCHAR NOT NULL SORTKEY,
     artist_id VARCHAR NOT NULL,
     title VARCHAR NOT NULL,
     year SMALLINT NOT NULL,
     duration NUMERIC(7,3) NOT NULL
  );
  """)

  # The position is stated to be split into its elements (lat, long) but I will use POINT instead
  artist_table_create = ("""
  CREATE TABLE IF NOT EXISTS artist_table(
     artist_id VARCHAR NOT NULL SORTKEY,
     artist_name VARCHAR NOT NULL,
     location VARCHAR,
     latitude NUMERIC(9,5),
     longitude NUMERIC(9,5)
  );
  """)

  # It is a bit strange to vaste space in the database to store hour, date, week, ... since it is implicit part of the TIMESTAMP and easily deducted from it. 
  time_table_create = ("""
  CREATE TABLE IF NOT EXISTS time_table(
     start_time TIMESTAMP NOT NULL SORTKEY,
     hour SMALLINT,
     day SMALLINT,
     week SMALLINT,
     month SMALLINT,
     year SMALLINT,
     weekday VARCHAR
  );
  """)

  # STAGING TABLES

  staging_events_copy = ("""
  COPY staging_events FROM {} credentials 'aws_iam_role={}' format as json {}
    STATUPDATE ON region 'us-west-2';
  """).format("use", "airflow", "configs")

  staging_songs_copy = ("""
    COPY staging_songs FROM {} credentials 'aws_iam_role={}' format as json 'auto'
    ACCEPTINVCHARS STATUPDATE ON region 'us-west-2';
  """).format("use", "airflow", "configs")

  # FINAL TABLES

  songplay_table_insert = ("""
  INSERT INTO songplay_table (start_time, user_id, song_id, artist_id, level,
                              session_id, location, user_agent)
  SELECT DISTINCT TIMESTAMP 'epoch' + events.ts/1000 * INTERVAL '1 second' AS start_time,
         events.userId AS user_id, events.level AS level, songs.song_id AS song_id,
         songs.artist_id AS artist_id, events.sessionId AS session_id,
         events.location AS location, events.userAgent AS user_agent
  FROM staging_events AS events
  JOIN staging_songs AS songs ON (events.artist = songs.artist_name) WHERE events.page = 'NextSong';
  """)

  user_table_insert = ("""
  INSERT INTO user_table (user_id, first_name, last_name, gender, level)
  SELECT  DISTINCT events.userId AS user_id, events.firstName AS first_name,
          events.lastName AS last_name, events.gender AS gender,
          events.level AS level
  FROM staging_events AS events
  WHERE events.page = 'NextSong';
  """)

  song_table_insert = ("""
  INSERT INTO song_table (song_id, artist_id, title, year, duration)
  SELECT  DISTINCT songs.song_id AS song_id, songs.artist_id AS artist_id,
          songs.title AS title, songs.year AS year, songs.duration AS duration
  FROM staging_songs AS songs;
  """)

  artist_table_insert = ("""
  INSERT INTO artist_table (artist_id, artist_name, location, latitude, longitude)
  SELECT  DISTINCT songs.artist_id AS artist_id, songs.artist_name AS artist_name,
          songs.artist_location AS location, songs.artist_latitude AS latitude, songs.artist_longitude AS longitude
  FROM staging_songs AS songs;
  """)

  time_table_insert = ("""
  INSERT INTO time_table (start_time, hour, day, week, month, year, weekday)
  SELECT  DISTINCT TIMESTAMP 'epoch' + events.ts/1000 * INTERVAL '1 second' AS start_time,
          EXTRACT(hour FROM start_time) AS hour,
          EXTRACT(day FROM start_time) AS day,
          EXTRACT(week FROM start_time) AS week,
          EXTRACT(month FROM start_time) AS month,
          EXTRACT(year FROM start_time) AS year,
          EXTRACT(week FROM start_time) AS weekday
  FROM staging_events AS events
  WHERE events.page = 'NextSong';
  """)

  # QUERY LISTS

  create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
  drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
  copy_table_queries = [staging_events_copy, staging_songs_copy]
  insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
