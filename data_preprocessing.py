

import asyncio
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google_trend_scraper import scrape_save_movies_trends
from imdb_rating_scraper import * 
import re

def create_imdb_movie_dataset(): 
    columns = ['Wikipedia movie ID', 'Freebase movie ID', 'name', 'release date', 
           'box office revenue', 'runtime', 'languages', 'countries', 'genres']

    df = pd.read_csv('MovieSummaries/movie.metadata.tsv', sep='\t')
    df.columns = columns

    imdb = pd.read_csv('MovieSummaries/imdb_ids.tsv', sep='\t')

    imdb.drop_duplicates(subset=['primaryTitle'], inplace=True)

    imdb.primaryTitle = imdb.primaryTitle.str.lower()
    df.name = df.name.str.lower()
    res = df.merge(imdb, 'inner', left_on='name', right_on='primaryTitle')

    res.to_csv('MovieSummaries/movies_imdb_ids.csv')