# from musixmatch import Musixmatch
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter
import collections
import string
import nltk
import numpy as np


from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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

def bm25(dict, query, vocabulary):
    results = {}
    constant = 1.2
    idf_dict = {}
    query_words = query.split()
    score=0.0
    stemmed_query_words = []
    ps = nltk.LancasterStemmer()

    for word in query_words:
        stemmed_query_words.append(ps.stem(word))
    # iterate through documents, which are the song lyrics
    for title, lyrics in dict.items():
        name = title
        doc = lyrics
        score = 0.0
        for word in stemmed_query_words:
            if word in doc and word in vocabulary:
                # print(word)
                # print("word")
                # calculate the tf for query and document
                tf_q = calculate_tf(stemmed_query_words, word)
                tf_d = calculate_tf(doc, word)
                # calculate idf if not present in idf_dic
                if word in idf_dict:
                    idf = idf_dict[word]
                else:
                    idf = calculate_idf(dict, word, idf_dict)
                numerator = (constant+1)*tf_d
                denominator = tf_d + constant
                # add to document score
                score+= tf_q*(numerator/denominator)*idf

        # update dictionary with score for this current doc

        results[name]=score
    return results

# tf helper function to count frequency of word in document
def calculate_tf(data, word):
    term_frequency = data.count(word)

    return term_frequency
# idf helper function to get document frequ
def calculate_idf(dict, word, idf_dict):
    M = len(dict)
    document_frequency=0
    for title, lyrics in dict.items():
        doc = lyrics
        if word in doc:
            document_frequency+=1
    idf = np.log((M+1)/(document_frequency))

    idf_dict[word]=idf
    return idf

# Helper function
# def recommended_songs(results):
#     top_ten_songs = []
#     for pair in results:
#         top_ten_songs.append(pair[0])
#     return top_ten_songs
    
# Searching function, takes in song_title, returns top 10 list
def recommend_songs(user_input):
    if user_input.lower() == 'quit':
        return []
    # if user_input not in title_to_lyrics:
    print("We are unable to find songs similar to", user_input)
    # else:      
    #     # print(user_input, "stemmed and parsed lyrics:", users_song)
    #     users_lyrics = title_to_lyrics[user_input]
    #     scores_dict = bm25(title_to_lyrics, users_lyrics, vocab_set)
    #     results = sorted(scores_dict.items(), key=lambda x:x[1], reverse=True)[1:10]
    #     top_ten_songs = []
    #     for pair in results:
    #         top_ten_songs.append(pair[0])
    #     results = top_ten_songs
    #     return results
    # print(results)

# def main(song_title):
# title_to_lyrics, word_counts, vocab_set = process_dataset()   

def main():
    # title_to_lyrics, word_counts, vocab_set = process_dataset() # takes 20 seconds to run

    # run everything in a loop so that user can input multiple song titles and get many
    # recs at once until they decide to quit
    while True:
        user_input = input("Enter a song title or 'quit' to quit: ") # Examples to test: Blank Space, # ​my tears ricochet, End Game
        # recommend_songs(user_input)
        # return recommend_songs(user_input, title_to_lyrics, title_to_lyrics[user_input], vocab_set)


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def recommend():
    user_input = request.form['textbox_data']
    # Process the user input (e.g., preprocess text)
    # processed_input = preprocess_text(user_input)
    # Generate recommendations based on the processed input
    recommendations = recommend_songs(user_input)  # Assuming the main function returns recommendations
    # Return the recommendations as a response
    return jsonify(recommendations)

#   recommendations = recommend_songs(song_title)
#   return jsonify(recommendations)

if __name__ == '__main__':
  app.run(debug=True, port=3000)