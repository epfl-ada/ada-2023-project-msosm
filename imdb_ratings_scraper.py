import asyncio
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from google_trend_scraper import scrape_save_movies_trends
import re
import time


def get_html_imdb_webpage(imdb_id, timestamp): 
    """fetch imdb webpage of specific movie closest to 
    to given timestamp from http://archive.org/wayback

    Args:
        imdb_id (str): movie id in the imdb database (e.g tt0414993)
        timestamp (str): timestamp of desired webpage YYYYMMDD (e.g. 20110628)

    Returns:
        bs4.BeautifulSoup: parsed html of webpage
    """

    imdb_url = 'www.imdb.com/title/' + imdb_id + '/'
    api_url = 'http://archive.org/wayback/available?url=' + imdb_url + '&timestamp=' + timestamp


    # request to wayback archive for movie url
    resp = requests.get(api_url)
    archive_url = resp.json()['archived_snapshots']['closest']['url']

    # print('archive url', archive_url)

    # request for imdb webpage
    resp = requests.get(archive_url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    time.sleep(11)

    return soup



def fetcher(string, date):

    result = []

    # different extractor base on date of the page
    if date <= 20110628:
        c = 1
    elif 20070209 < date <= 20110628:
        c = 2
    elif 20110628 < date <= 20110720:
        c = 3
    else:
        c = 4

    # Try for correct date. If error, try for the next range. If still error, try the previous range.
    try:
        result = extract_vote_number_ratings(c, string)
        # print('c=',c, 'date', date)
    except Exception as e:
        print('c=',c, e)
        try:
            result = extract_vote_number_ratings(c + 1, string)
            # print('c=',c +1 , 'date', date)
        except Exception as e:
            print('c=',c +1 , e)
            try:
                result = extract_vote_number_ratings(c - 1, string)
                # print('c=',c -1, 'date', date)
            except Exception as e:
                # print('c=',c -1, e)
                print(f"Unable to retrieve data for  ({date}): exception {e}")
    
    return result


def extract_vote_number_ratings(num, bs4_html):
    result = []

    if num == 1 or num == 0:

        # Ref url: http://web.archive.org/web/20070209064101/https://www.imdb.com/title/tt0120338/
        essential = str(bs4_html.find('table'))
        rating_pattern = re.compile(r'(\d\.\d+)\/10', re.MULTILINE)
        numvotes_pattern = re.compile(r'(\d+)(?:,(\d+))?\s*votes', re.MULTILINE)
        match = rating_pattern.search(essential)
        result.append(float(match.group(1)))

        match = numvotes_pattern.search(essential)
        numvotes = int(match.group(1) + (match.group(2) if match.group(2) else ''))
        result.append(numvotes)


    elif num == 2:
        # Ref url: http://web.archive.org/web/20070816164703/http://www.imdb.com:80/title/tt0414993
        essential = str(bs4_html)
        rating_pattern = re.compile(r'(\d\.\d+)\/10', re.MULTILINE)
        numvotes_pattern = re.compile(r'(\d+)(?:,(\d+))?\s*votes', re.MULTILINE)
        
        match = rating_pattern.search(essential)
        result.append(float(match.group(1)))

        
        match = numvotes_pattern.search(essential)
        numvotes = int(match.group(1) + (match.group(2) if match.group(2) else ''))
        result.append(numvotes)

    elif num == 3:
        # Ref url: http://web.archive.org/web/20110720180900/http://www.imdb.com:80/title/tt0414993/
        span_tag = bs4_html.find('span', {'itemprop': 'ratingValue'})
        result.append(float((span_tag.text.strip())))


        essential = str(bs4_html)
        numvotes_pattern = re.compile(r'(\d+)(?:,(\d+))?\s*votes', re.MULTILINE)
        
        match = numvotes_pattern.search(essential)
        numvotes = int(match.group(1) + (match.group(2) if match.group(2) else ''))
        result.append(numvotes)

    elif num == 4:
        # Ref url: http://web.archive.org/web/20110830045202/http://imdb.com:80/title/tt0414993/
        span_tag = bs4_html.find('span', {'itemprop': 'ratingValue'})
        if span_tag is None: 
            span_tag = bs4_html.find('span', class_='rating-rating')


        result.append(float((span_tag.text.strip().replace('/10', ''))))


        span_tag = bs4_html.find('span', {'itemprop': 'ratingCount'})
        if span_tag is None: 
            votes_anchor = bs4_html.find('a', href="ratings") #.find('a', onclick=lambda x: 'ratings' in x)
            votes_text = votes_anchor.text
            numvotes = re.search(r'\d+', votes_text).group()

        else: 
            numvotes = int(span_tag.text.strip().replace(',', ''))

        result.append(numvotes)

    return result

def scraper_review_next_and_five_years(imdb_id, pub_year): 
    """scrape ratings and number of voters from imdb for one year and five year 
    after publication 

    Args:
        imdb_id (string): movie id
        pub_year (datetime): publication year

    Returns:
        scraped_dates, ratings, num_voters_list: lists
    """

    ratings = []
    num_voters_list = []
    scraped_dates = []

    # most recent movie in the df is end of 2012, so both dates will be in the past
    next_year = pub_year + timedelta(days=365)
    five_years = pub_year + timedelta(days=365*5)

    for date in [next_year, five_years]: 

        try:
            bs4_html = get_html_imdb_webpage(imdb_id, date)
            rating, num_voters = fetcher(bs4_html, int(date))

            ratings.append(rating)
            num_voters_list.append(num_voters)
            scraped_dates.append(date)

        except ValueError as e: 
            print(f"couldn't scrape for {date}: exception {e}")

    return scraped_dates, ratings, num_voters_list
    



def generate_date_list():
    # Get the current date
    current_date = datetime(2020, 11, 11)

    # Set the start date to 2005-01-01

    start_date = datetime(2005, 1, 1)

    # Initialize an empty list to store the formatted dates
    date_list = []

    # Generate dates from 2005 to the current year
    while start_date <= current_date:
        formatted_date = start_date.strftime("%Y%m%d")
        date_list.append(formatted_date)

        # Move to the next day
        start_date += timedelta(days=500)

    return date_list



def scrape_through_the_years(imdb_id): 
    """scrape reviews every year from 2004 to present

    Args:
        imdb_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    ratings = []
    num_voters_list = []
    scraped_dates = []

    dates = generate_date_list()

    for date in dates: 

        try:
            bs4_html = get_html_imdb_webpage(imdb_id, date)
            rating, num_voters = fetcher(bs4_html, int(date))

            ratings.append(rating)
            num_voters_list.append(num_voters)
            scraped_dates.append(date)

        except ValueError as e: 
            print(f"couldn't scrape for {date}")

    return scraped_dates, ratings, num_voters_list






if __name__ == "__main__": 
    # date = '20181001'
    bs4_html = get_html_imdb_webpage('tt0048644', '20110708')


    print(fetcher(bs4_html, int(20110708)))
    # rating_span = bs4_html.find('span', class_='rating-rating')
    # rating = rating_span.text
    # print(rating)




#     dates, ratings, num_voters = scrape_through_the_years('tt0002894')
# # 
#     print('dates', dates)
#     print('ratings', ratings)
#     print('number of voters', num_voters)


    # res = pd.read_csv('MovieSummaries/movies_imdb_ids.csv')

    # result_df = pd.DataFrame()

    # for const in res.tconst.values[:3]: 
    #     try: 
    #         dates, ratings, num_voters = scrape_through_the_years(const)
    #     except Exception as e: 
    #         print(e)
    #     print(const, len(dates))
    #     df = pd.DataFrame([b, c], columns=a)
    #     result_df = pd.concat([df, result_df], ignore_index=True, sort=False)

    # result_df

