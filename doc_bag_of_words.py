from similarity import preprocess_text
import load_functions as lf
import pandas as pd
import numpy as np

data_folder = './data/MovieSummaries/'
(movie_metadata, character_metadata, name_clusters, plot_summaries, test_data) = \
    lf.load_movie_summaries(data_folder)


plot_similarity = plot_summaries
plot_evolution = plot_summaries
plot_similarity['count_words'] = plot_similarity.apply(lambda x: len(str(x['plot']).split()), axis=1)

# Drop plots with less than 200 words
plot_similarity.drop(plot_similarity[plot_similarity['count_words'] < 200].index, inplace= True)

df_split = np.array_split(plot_similarity, 10)

i = 0
for df in df_split:
    print(i)
    df['preprocessed_text'] = df.apply(lambda x: pd.Series([preprocess_text(x['plot'])]), axis=1)

    # Apply a transformation to expand each dictionary into its own series of columns
    doc_words_df = df['preprocessed_text'].apply(pd.Series)
    doc_words_df['wiki_movie_id'] = df['wiki_movie_id']
    doc_words_df.set_index('wiki_movie_id')

    # Replace NaN values with 0, as NaN means the word did not appear in that document
    doc_words_df = doc_words_df.fillna(0)

    # Convert float values to int, as frequencies are whole numbers
    doc_words_df = doc_words_df.astype(int)

    doc_words_df.to_pickle('data/doc_words_df_' + str(i) +'.pkl')
    i = i + 1
