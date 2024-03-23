from musixmatch import Musixmatch
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter
import string
import nltk

ps = nltk.LancasterStemmer()

# Function to preprocess text
# Remove stop-words, transform words to lower-case, remove punctuation and numbers, and excess
# whitespaces (keeping only one space that separates words). 
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation and numbers
    c = []
    for letter in text:
        if letter not in string.punctuation and not letter.isdigit():
            c.append(letter)

    text = ''.join(c)
    
    # Remove excess whitespaces
    text = ' '.join(text.split())
   
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
   
    text = text.split()
    filtered_text = [ps.stem(word) for word in text if word not in stop_words]
    filtered_text = ' '.join(filtered_text)
    return filtered_text

api_key = "f8e4df4dd30ca640559a3e0010c6980f"
musixmatch = Musixmatch('f8e4df4dd30ca640559a3e0010c6980f')
# print(musixmatch.chart_artists(1, 1))
# print(musixmatch.track_lyrics_get(279919027))

# print(musixmatch.artist_get(32153100))
# print(musixmatch.chart_tracks_get(2, 1, 1))

df = []
tracks = musixmatch.chart_tracks_get(1, 3, 1)
tracks_list = tracks['message']['body']['track_list']
# print(tracks_list)
# print(tracks['message']['body']['track_list'][1]['track']['track_id'])

# get top tracks
for track in tracks_list: # artist name, genre name, song name, lyrics, 
    # print(track['track']['track_id'])
    
    song_id = track['track']['track_id']
    song_name = track['track']['track_name']
    artist_name = track['track']['artist_name']
    genre_name = track['track']['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
    lyrics = musixmatch.track_lyrics_get(song_id)['message']['body']['lyrics']['lyrics_body']
    # print(lyrics)
    lyrics = lyrics.split("\n")
    for i, lyric_line in enumerate(lyrics):
        if lyric_line == "******* This Lyrics is NOT for Commercial use *******":
            lyrics[i] = ""
        lyrics[i] = preprocess_text(lyric_line)
    # print(' '.join(lyrics))
    lyrics = ' '.join(lyrics)
    doc = [artist_name, genre_name, song_name, lyrics]
    df.append(doc)

# print(df)

dataframe = pd.DataFrame(df, columns=['artist_name', 'genre_name', 'song_name', 'lyrics'])
dataframe.to_csv('processed_data.csv')