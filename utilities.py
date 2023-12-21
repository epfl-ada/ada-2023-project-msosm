import pandas as pd
import numpy as np
import statsmodels.api as sm

import matplotlib.pyplot as plt
import seaborn as sns


def plot_25_movies_through_time(df, feature): 

    # movies_info_ratings = importance_over_time_df_adjusted[~importance_over_time_df_adjusted.runtime.isna()]
    sorted_movie_data = df.sort_values(by=['year', 'numVotes'], ascending=[True, False])

    # Use groupby to keep the top 25 movies for each year
    top_25_movies = sorted_movie_data.groupby('year').head(25)
    top_25_movies = top_25_movies[top_25_movies.year > 1930]

    window_size = 5
    top_25_movies_grouped = top_25_movies.groupby('year').mean()[feature].rolling(window=window_size).mean()
    top_25_movies_grouped_std = top_25_movies.groupby('year').std()[feature].rolling(window=window_size).mean()

    # Plotting the data with a regression line and confidence interval
    sns.lineplot(x='year', y=feature, data=pd.DataFrame(top_25_movies_grouped), ci=95,)

    lower_bound = top_25_movies_grouped - top_25_movies_grouped_std * 1.96 / 5
    upper_bound = top_25_movies_grouped + top_25_movies_grouped_std * 1.96  / 5
    plt.fill_between(top_25_movies_grouped.index, lower_bound, upper_bound, alpha=.3)

    plt.xlabel('Year')