import pandas as pd
import math
import os
from datetime import datetime

def load_movie_summaries(data_folder):
    # data_folder = './data/MovieSummaries/'
    movie_metadata = pd.read_table(data_folder + 'movie.metadata.tsv', header=None)
    movie_metadata.columns = ['wiki_movie_id','free_movie_id','movie_name','release_date','box_office_revenue', 'runtime','languages','countries','genres']
    character_metadata = pd.read_table(data_folder + 'character.metadata.tsv', header=None)
    character_metadata.columns = ['wiki_movie_id','free_movie_id','release_date','character_name','actor_birth_date','actor_gender','actor_height','actor_ethnicity','actor_name','actor_age','free_character_actor_map_id','free_character_id','free_actor_id']
    name_clusters = pd.read_csv(data_folder + 'name.clusters.txt', sep="\t", header=None)
    name_clusters.columns = ['character_name', 'free_character_actor_map_id']
    plot_summaries = pd.read_csv(data_folder + 'plot_summaries.txt', sep='\t', header=None)
    plot_summaries.columns = ['wiki_movie_id', 'plot']
    test_data = pd.read_csv(data_folder + 'tvtropes.clusters.txt', sep='\t', header=None)
    test_data.columns = ['character_type', 'dictionary']
    test_data['dictionary'] = test_data['dictionary'].apply(eval)
    test_data['character_name'] = test_data.dictionary.apply(lambda x: x['char'])
    test_data['movie_name'] = test_data.dictionary.apply(lambda x: x['movie'])
    test_data['free_character_actor_map_id'] = test_data.dictionary.apply(lambda x: x['id'])
    test_data['actor_name'] = test_data.dictionary.apply(lambda x: x['actor'])
    
    return (movie_metadata, character_metadata, name_clusters, plot_summaries, test_data)

def extract_year(date_str):  # float year
    if date_str is None or date_str == "":
        return None  # or handle it in your desired way

    # Check if the input is NaN (float NaN)
    if isinstance(date_str, float) and math.isnan(date_str):
        return None  # Handle NaN as needed

    # Convert the input to a string if it's a float
    if isinstance(date_str, float):
        date_str = str(date_str)  # Assuming it's a float representing a year

    try:
        date = datetime.strptime(date_str, "%Y")
        return date.year
    except ValueError:
        try:
            date = datetime.strptime(date_str, "%Y-%m")
            return date.year
        except ValueError:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                return date.year
            except ValueError:
                return None
            
            
def load_scripts(folder_path, movie_names):
    scripts = {}
    for filename in os.listdir(folder_path):
        # check if the file matches the specified format and is in the provided dataset, construct the path
        if filename.startswith('Script_') and filename.endswith('.txt'):
            movie_name_from_filename = filename[len('Script_'):-len('.txt')]
            if movie_name_from_filename in movie_names:
                file_path = os.path.join(folder_path, filename)
            
                # read from the file
                with open(file_path, 'r') as file:
                    file_contents = file.read()
                    scripts[movie_name_from_filename] = file_contents

    return scripts