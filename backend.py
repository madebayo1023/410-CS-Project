from musixmatch import Musixmatch
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter
import string
import nltk

def get_data():
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

    df = []
    for i in range(1):
        smth = musixmatch.catalogue_dump_get('test')
        print(smth)
        tracks = musixmatch.chart_tracks_get(1, 1000, 1)
        tracks_list = tracks['message']['body']['track_list']
        for i, track in enumerate(tracks_list): # artist_name, artist_id, song_name, song_id, genre_name, lyrics
            song_id = track['track']['track_id']
            song_name = track['track']['track_name']
            artist_name = track['track']['artist_name']
            artist_id = track['track']['artist_id']
            genre_name = ""
            try:
                genre_name = track['track']['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
            except IndexError:
                print(i, track['track']['primary_genres']['music_genre_list'], "will manually write these in")  # only 2 do not have a genre, causing issues
            lyrics = musixmatch.track_lyrics_get(song_id)['message']['body']['lyrics']['lyrics_body']
            lyrics = lyrics.split("\n")
            for i, lyric_line in enumerate(lyrics):
                if lyric_line == "******* This Lyrics is NOT for Commercial use *******":
                    lyrics[i] = ""
                lyrics[i] = preprocess_text(lyric_line)
            lyrics = ' '.join(lyrics)
            doc = [artist_name, artist_id, song_name, song_id, genre_name, lyrics]
            df.append(doc)

    dataframe = pd.DataFrame(df, columns=['artist_name', 'artist_id', 'song_name', 'song_id', 'genre_name', 'lyrics'])
    dataframe.to_csv('processed_data.csv')

def main():
    get_data()
    # print("Enter a song title:")
    # user_input = input("Enter something: ")
    # # check if in dataset, otherwise search it
    # print(user_input)
    # song_info = musixmatch.track_search(q_track='Who\'s Afraid of Little Old Me?')






if __name__ == "__main__":
    main()