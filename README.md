# Frame by Frame: The Kaleidoscopic Evolution of Cinema Over the Decades

## Abstract

Movies have transformed significantly in the last century progressing from silent black-and-white films to today's vibrant and captivating productions. With this project, we aim to gain a deeper understanding of these changes with an analysis of movies from different points of view. Firstly, we'll discuss the changes in (the complexity of) movie plots and the increase/decrease of similarity between plots over time. Secondly, we'll look at the movie metadata to analyze what makes a movie age faster (and be forgotten more quickly) and which are the features with lead to higher revenues in different historical periods.

## Research questions

- Did the complexity of movie dialogues decrease over time? Can we find a correlation between the simplification of movies and the rise of social media and instatenuos messaging?
- Is it true that movies have become more similar in recent years?
- Which movie characteristic makes it age more slowly and stay popular for longer?
- How did movie plots change over time?
- How did the impact of each feature on revenue change over time? Which feature became more or less relevant through the years?

## Additional datasets

#### Dataset imdb ratings over time

In order to understand how the ratings of certain movies has evolved over time, we used an the API provided by [WaybackMachine](https://archive.org/help/wayback_api.php) to get a snapshot of the [IMBD.com](https://www.imdb.com/) page of each movie one year and five years after the release. In this way we were able to obtain the rating and the number of people who voted, while associating them with the IMBD identifier provided in the [IMDB database](https://datasets.imdbws.com/title.basics.tsv.gz) and with the original dataset through the name of the movie. [Movies budget](https://www.kaggle.com/datasets/danielgrijalvas/movies?select=movies.csv) were obtained from Kaggle. In order to adjust for inflation we also downloaded the [CPI data](https://www.bls.gov/cpi/data.htm) from the U.S Bureau of Labour and Statistics.

## Methods

### Evolution movie plots and plot originality

#### Plot preprocessing

First, we have to preprocess the textual data. For this purpose we use the spacy library, making use of a natural language model. The major preprocessing steps we use are the following:

- **Tokenization:** We transform the represantation of the plot, currently one long string, into a list of tokens (words, punctuation, ..). Only tokens with alphabetic characters, i.e. regular words, are kept. All other tokens are dropped
- **Named entity recognition:** We also extract all the named entities used in the plot. If these entities are one word person names, like Harry or Emma, we drop them from the list of tokens. This is done because the names of the characters are not significant to the plot. If for example in two very different movies plot-wise, the main character of the movie has the same name, we don't want the LDA to see them as similar because of the same word (the main characters name) occurs a lot in both. However, multi-word named entities, like "New York" were added seperately as "extra tokens".
- **Lemmatization:** Each token is transformed into its base form. Like this occurences of e.g. kill versus kills, have the same influence
- **Casefolding:** All tokens are transformed into their lowercase version.
- **Stopword removal:** Stopwords (very common words) are removed. For this we used a standard list of english stopwords provided by spacy. Furthermore, when doing are analysis, we found that also the words "film" and "tell" were very frequently used in plot summaries and were not really representative of the plot. Therefore these were added to the list of stopwords.
- **Adding bigrams:** We also add bigrams that occur frequently in the corpus, to the list of tokens for each plot.

Furthermore, after the plots are preprocessed we will represent them as a Bag of Words. An extra preprocessing step is also performed, namely very frequent and extremely rare words are removed. Specifically, words that occur in more then 33% of the plots, are removed. Multiple values for this minimum frequency were tried and a value of 33% produced the best results. Also words that occur in only 5 plots or less, are too infrequent and don't add any value, and are thus removed. The resulting Bag of Words representation of the plots will be used by the LDA algorithm.

#### LDA

Now we can finally get into the LDA analysis! For this we use the gensim library. LDA computes topics as probability distributions over words, and then represents the text documents as probability distributions over these topics. An important parameter that we have to set ourselves is the amount of topics. We will perform LDA for 6, 8 and 10 topics. Finally, after meticulous evalution we decide to proceed with the analysis with the 6-topic LDA. Dive into our Jupyter Notebook to figure out what are the found topics.

### Evolution of movie topic

### Plot originality

After performing the LDA, we obtain a 6 component vector with a probability distribution for each topic. We have decided to compute plot originality using **cosine similarity** using this vector. For every movie, we compute the cosine similarity to those released in the same year, by that we aim to grasp at how original were movies made in that year, or on the other end how stereotypical.

The interpretation obtained might be a bit counter intuitive. One can expect that movies with more than one topic to be more similar to others since they will have more in common. We have defined those movies as original since they represent a mix of topics, creating a unique thematical narrative. On the other hand, those movies with low cosine similarity will be pure stereotypical movies being only close to the ones of the same topic. For more information on the method dive into the Jupyter Notebook to understand furthermore how we use it and the results we obtain.

### Plot complexity

In our endeavor to dissect the intricacies of cinematic storytelling, our focus lies on two dimensions. The first entails the establishment of a complexity score derived from the ratio of plot summary words to film runtime. Simultaneously, our second initiative involves the definition of° various complexity scores as a ratio of complex words to the total number of words.

### Movie metadata preprocessing

Firstly we removed all the movies without movie_box_office_reveneue (attempts to find datasets with additional box_office_revenue weren’t successful). We extracted the year from all the dates. Then we merged the movie.metadata dataset with the imbd one. Finally, we extracted the features that were encoded in a dictionary (language, genre, country) and added them to the dataset with onehot encoding.

### Movie aging

For this part, we will all the provided dataset along with IMDB pages scraped from [WaybackMachine](https://archive.org/help/wayback_api.php). From these scraped pages we were able to obtain the past reviews of movies. We took the difference between the ratings for one and five years after release. This shows which movie became more or less popular over time. Then we regressed the metadata of the movies on the difference in ratings to determine which features have greater influence on the popularity of a movie over time.

### Most influential feature for revenue over time

Finally, to answer the question of which features had a higher influence on the revenue through the years we grouped by decades. Then we regressed over the revenue in each of these groups and sorted the coefficient to understand which were the more relevant features in each year group.

## Timeline and organization

### Executed timeline

Steps ...: **Deadline Milestone 2 17.11.2022**

*24.11.2023  - Perform initial analysis*

*28.11.2023 - Pause project work*

*01.12.2023: Deadline Homework 2*

*15.12.2023: Complete notebook and start writing the blog*

*18.12.2023 - Finalize data story*

Step ...: **Deadline Milestone 3 22.12.2023**

### Organization within the team

- **Oriol**

  - Plot similarity
  - Analyze the evolution of the emotional arc
- **Stefano V**

  - Finish scraping of IMDb ratings
  - Regress on newly scraped ratings
  - Find other methods to determine feature importance
- **Stefano C**

  - Plot complexity
  - Write blog story
- **Max**

  - Fully implement LDA
  - Perform basic K-means clustering on bag-of-words vectors
  - Analyze movies' plot evolution using K-means clustering
  - Analyze movies' plot evolution using topic-based representation generated by LDA
- **Michele**

  - Exploratory Data Analysis
  - Regress on groups of ten years
