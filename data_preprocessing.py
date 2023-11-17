

import asyncio
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
from google_trend_scraper import scrape_save_movies_trends
from imdb_rating_scraper import * 
from datetime import timedelta
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


def clean_movie_dataset(drop_no_revenue): 
    columns = ['Wikipedia movie ID', 'Freebase movie ID', 'name', 'release date', 
        'box office revenue', 'runtime', 'languages', 'countries', 'genres']

    df = pd.read_csv('MovieSummaries/movie.metadata.tsv', sep='\t')
    df.columns = columns

    df.name = df.name.str.lower()
    if drop_no_revenue: 
        box_office  = df.loc[~df['box office revenue'].isna()].copy(deep = True)
    else: 
        box_office = df.copy(deep=True)

    dates = box_office['release date'].apply(lambda x : pd.to_datetime( x, format='%Y-%m-%d', errors='coerce')).copy(deep = True)
    box_office.loc[:,'release date'] = dates

    box_office = box_office.dropna(subset=['release date']).copy()

    return box_office


def standardize_dates(dataset, days_gap): 
    start_range = datetime(1920, 1, 1)
    end_range = datetime(1920, 1, 1) + timedelta(days_gap)
    max_date = dataset['release date'].max()

    dataset = dataset.loc[dataset['release date'] >= start_range].copy(deep = True)

    while start_range < max_date: 
        dataset.loc[(dataset['release date'] >= start_range) & (dataset['release date'] < end_range), ('release date')]  = start_range
        start_range = end_range
        end_range = end_range + timedelta(days_gap)

