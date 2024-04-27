from musixmatch import Musixmatch
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter
import collections
import string
import nltk

"""
    Processes a document / query.

    Args:
        text (string): the document / query to be processed

    Returns:
        filtered_text: the processed and stemmed document / query
"""
def preprocess_text(text):
        ps = nltk.LancasterStemmer()
        # Remove punctuation and numbers
        c = []
        # print(text)
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
        return filtered_text.lower()

"""
    Processes the dataset "dataset.csv".

    Returns:
        dict: a dictionary song title as a key to lyrics as the value.
        word_counts: a collection (like an array of tuples) where the first pair value is the stemmed and parsed word
                     and the second pair value is the frequency of the word in the entire collection of documents.
        vocab_set: a set of all the words in the collection (no repeats)
"""
def process_dataset():
    df = pd.read_csv("dataset.csv")
    df = df.dropna()
    dict = {}
    vocab, word_counts, vocab_set = [], [], []
    for row in (range(len(df))):
        lyrics = preprocess_text(df.iloc[row]['Lyric'])
        dict[df.iloc[row]['Title']] = lyrics
        vocab += lyrics.split()
    word_counts = collections.Counter(vocab) # word to frequency
    vocab_set = set(vocab) # set of all the words in the dictionary
    return dict, word_counts, vocab_set

def main():
    title_to_lyrics, word_counts, vocab_set = process_dataset() # takes 20 seconds to run

    # run everything in a loop so that user can input multiple song titles and get many
    # recs at once until they decide to quit
    while True:
        user_input = input("Enter a song title or 'quit' to quit: ") # Examples to test: Blank Space, # ​my tears ricochet, End Game
        if user_input.lower() == 'quit':
            break
        if user_input not in title_to_lyrics:
            print("We are unable to find songs similar to", user_input)
        else:
            # TODO 
                # call bm25 tf-idf function to return top 10 similar songs, using the lyrics of the entered song title as the query
                # we are assuming that the songs entered exist in the data set + match case in dataset exactly
            print(user_input, "stemmed and parsed lyrics:", title_to_lyrics[user_input])

if __name__ == "__main__":
    main()


# OLD CODE TO IGNORE

# def get_data():
#     ps = nltk.LancasterStemmer()

#     # Function to preprocess text
#     # Remove stop-words, transform words to lower-case, remove punctuation and numbers, and excess
#     # whitespaces (keeping only one space that separates words). 
#     def preprocess_text(text):
#         # Convert to lowercase
#         text = text.lower()
        
#         # Remove punctuation and numbers
#         c = []
#         for letter in text:
#             if letter not in string.punctuation and not letter.isdigit():
#                 c.append(letter)

#         text = ''.join(c)
        
#         # Remove excess whitespaces
#         text = ' '.join(text.split())
    
#         # Remove stopwords
#         stop_words = set(stopwords.words('english'))
    
#         text = text.split()
#         filtered_text = [ps.stem(word) for word in text if word not in stop_words]
#         filtered_text = ' '.join(filtered_text)
#         return filtered_text

#     api_key = "f8e4df4dd30ca640559a3e0010c6980f"
#     musixmatch = Musixmatch('f8e4df4dd30ca640559a3e0010c6980f')

#     df = []
#     for i in range(1):
#         smth = musixmatch.catalogue_dump_get('test')
#         print(smth)
#         tracks = musixmatch.chart_tracks_get(1, 1000, 1)
#         tracks_list = tracks['message']['body']['track_list']
#         for i, track in enumerate(tracks_list): # artist_name, artist_id, song_name, song_id, genre_name, lyrics
#             song_id = track['track']['track_id']
#             song_name = track['track']['track_name']
#             artist_name = track['track']['artist_name']
#             artist_id = track['track']['artist_id']
#             genre_name = ""
#             try:
#                 genre_name = track['track']['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
#             except IndexError:
#                 print(i, track['track']['primary_genres']['music_genre_list'], "will manually write these in")  # only 2 do not have a genre, causing issues
#             lyrics = musixmatch.track_lyrics_get(song_id)['message']['body']['lyrics']['lyrics_body']
#             lyrics = lyrics.split("\n")
#             for i, lyric_line in enumerate(lyrics):
#                 if lyric_line == "******* This Lyrics is NOT for Commercial use *******":
#                     lyrics[i] = ""
#                 lyrics[i] = preprocess_text(lyric_line)
#             lyrics = ' '.join(lyrics)
#             doc = [artist_name, artist_id, song_name, song_id, genre_name, lyrics]
#             df.append(doc)

#     dataframe = pd.DataFrame(df, columns=['artist_name', 'artist_id', 'song_name', 'song_id', 'genre_name', 'lyrics'])
#     dataframe.to_csv('processed_data.csv')