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

# ModelTests module to compare VSM and BM25
class ModelTests(unittest.TestCase):
    def test_one(self):
        song = "Blank Space"
        bm_top = recommend_songs(song)
        vsm_top = vsm_recommend_songs(song)
        print("BM: " + str(bm_top))
        print("VSM: " + str(vsm_top))
        self.assertEqual(len(bm_top), len(vsm_top))

    def test_two(self):
        song = "End Game"
        bm_top = recommend_songs(song)
        vsm_top = vsm_recommend_songs(song)
        print("BM: " + str(bm_top))
        print("VSM: " + str(vsm_top))
        self.assertEqual(len(bm_top), len(vsm_top))

    def test_basic(self):
        songs = ["Hello", "Adventure of a Lifetime", "Levitating"]
        for song in songs:
            bm_top = recommend_songs(song)
            vsm_top =  vsm_recommend_songs(song)
            self.assertEqual(len(bm_top), len(vsm_top))

# Results module tests:
# Top 1 result is user song
# Top results's top songs contain user song
# Remixed songs are somtimes ranked closely
class ResultsTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(recommend_songs(""), ['We are unable to find songs similar to '])

    # Test 5 snogs that the first song returned should be the same as the query song
    def test_basic_run(self):
        songs = ["Blank Space", "Hello", "End Game", "Adventure of a Lifetime", "Levitating"]

        for song in songs:
            top = recommend_songs(song)
            self.assertEqual(len(top), 10)
    
    def test_top_song(self):
        songs = ["How You See the World", "Wildest Dreams / Enchanted", "Tucked", "Blank Space"]
        songs = random.sample(list(title_lyric_dict.keys()), 5)
        
        for song in songs:
            top = recommend_songs(song)
            self.assertEqual(song, top[0], song + "'s top 1 song is incorrect")
    
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

    def test_songs_contain(self):
        self.assertEqual(5 - 3, 2)
        songs = ["New Rules (KREAM Remix)",
                 "Special",
                 "1000 Doves",
                 "Hot n Cold"]
    
        for song in songs:
            top = recommend_songs(song)
            top_list = recommend_songs(top[1])

            self.assertTrue(song in top_list, song + " not in " + top[2])

if __name__ == '__main__':
    unittest.main()
