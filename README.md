# 410-CS-Project

dataset: https://www.kaggle.com/datasets/deepshah16/song-lyrics-dataset


To run the application:
- clone the repository into your desired folder location.
- install all dependencies included in the requirements.txt file
- run 'python app.py' to start up the applictaion on port 3000 on your local computer (http://127.0.0.1:3000/).
- once the application starts up, you can enter any song of your choice to get recommendations based on it!
- we assume that the song title is in dataset & the query entered matches it exactly. Some example test queries are:
   * Blank Space
   * End Game
   * Hello
   * Don’t Hurt Yourself
   * Hotline Bling
   * Unforgettable
   * A Thousand Bad Times

To run tests:
- run 'python test.py'
- run 'python -m unittest tests.MODULE_NAME'
   where MODULE_NAME can be:
   - DatasetTests
   - DataTests
   - ModelTests
   - ResultsTests

To use BM25 TF-IDF model:
- in 'app.py' change line 197 to 'recommendations = recommend_songs(user_input)'
- Comment out line 142 so that it is: # title_to_lyrics_vector = create_data_vector(title_to_lyrics, vocab_set) to help with run time

To use VSM bit vector model:
- in 'app.py' change line 197 to 'recommendations = vsm_recommend_songs(user_input)'
- Un-comment line 142 so that it is: title_to_lyrics_vector = create_data_vector(title_to_lyrics, vocab_set)
