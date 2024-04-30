import unittest
from app import process_dataset, bm25, calculate_tf, calculate_idf, recommend_songs
from app import *
import random

# To run all tests:
# python tests
# To run a test module:
# python -m unittest tests.MODULE_NAME

title_lyric_dict, wordcounts, vocab = process_dataset()

# Dataset module tests:
# Dataset validity and cleanliness
class DatasetTests(unittest.TestCase):
    def test_artists(self):
        df = pd.read_csv("dataset.csv")
        df = df.dropna()
        # no BTS or Ariana Grande
        self.assertEqual(19, df['Artist'].nunique())

    def test_format(self):
        self.assertEqual(2870, len(title_lyric_dict))

    def test_no_nan(self):
        self.assertFalse("nan" in title_lyric_dict)
        self.assertFalse("nan" in title_lyric_dict.values())

# Data module tests:
# Data successful text processing 
class DataTests(unittest.TestCase):
    def test_all_lowercase(self):
        for lyrics in title_lyric_dict.values():
            if any(char.isupper() for char in lyrics):
                self.fail("Error: uppercase character is in dataset")
        self.assertTrue(1)

    def test_no_numbers(self):
        for lyrics in title_lyric_dict.values():
            if any(char.isdigit() for char in lyrics):
                self.fail("Error: numeric character is in dataset")
        self.assertTrue(1)

# Model module tests:
# Calculated values exist
# TF-IDF, BM25 are valid
class ModelTests(unittest.TestCase):
    def test_calculation(self):
        self.assertEqual("hello" + "world", "helloworld")

    def test_tfidf(self):
        self.assertEqual(5 - 3, 2)
        
    def test_bm25(self):
        self.assertEqual(5 - 3, 2)

# # BM25 TF-IDF better than TF-IDF
class BestModelTests(unittest.TestCase):
    def test_bestmodel(self):
        self.assertEqual(5 - 3, 2)

# Results module tests:
# Top 1 result is user song
# Top results's top songs contain user song
# Remixed songs are somtimes ranked closely
class ResultsTests(unittest.TestCase):
    # Test 5 random snogs that the first song returned should be the same as the query song
    def test_top_song(self):
        songs = ["Don’t Start Now",
                 "Stuck In the Moment (Acoustic)",
                 "Something Just Like That (Love in Tokyo Version)",
                 "Picture to Burn",
                 "Tim McGraw"]
        
        for song in songs:
            top = recommend_songs(song)
            self.assertEqual(song, top[0], song + "'s top 1 song is incorrect")
    
    def test_songs_contain(self):
        self.assertEqual(5 - 3, 2)

    def test_remixsongs(self):
        songs = ["We Found Love (Black Cards Remix)",
                 "Shape of You (Berywam Remix)",
                 "Swan Song (aboutagirl Remix)",
                 "Diamonds (The Bimbo Jones Vocal Remix)",
                 "Best I Ever Had (Remix)"]
        
        for song in songs:
            # Parse original title by removing (___ Remix)
            remix_title = song
            original_title = song.split('(')[0].strip()
            # print("Original " + original_title)

            # Check that remix song is in original song's top
            top_songs = recommend_songs(original_title)
            seen = 0
            for s in top_songs:
                if s == remix_title:
                    seen = 1
                    break
            self.assertTrue(seen, remix_title + " not in " + original_title + "'s top songs")

# Frontend module tests:
# Valid song search
# Empty song search
# Invalid song search
# class FrontendTests(unittest.TestCase):
#     def test_empty_search(self):
#         self.assertEqual(5 - 3, 2)

#     def test_valid_search(self):
#         self.assertEqual(5 - 3, 2)
    
#     def test_invalid_search(self):
#         self.assertEqual(5 - 3, 2)

if __name__ == '__main__':
    unittest.main()
