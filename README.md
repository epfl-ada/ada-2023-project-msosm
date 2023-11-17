# Film Metamorphosis: from silent to ....?

## Abstract

Movies have transformed significantly in the last century progressing from silent black-and-white films to today's vibrant and captivating productions. With this project, we aim to gain a deeper understanding of these changes with an analysis of movies from different points of view. Firstly, we'll discuss the changes in the complexity of the plots and the increase/decrease of similarity between plots over time. Secondly, we'll look at the movie metadata to analyze what makes a movie age faster (and be forgotten more quickly) and which are the features with lead to higher revenues in different historical periods. 

## Research questions

- Did the complexity of movie dialogues decrease over time? Can we find a correlation between the increase in smartphone usage and the decrease in attention span? 
- Is it true that movies have become more similar in recent years? 
- Which movie characteristic makes it age more slowly and stay popular for longer?
- How did movie plots change over time? 
- How did the impact of each feature on revenue change over time? Which feature became more or less relevant through the years? 


## Additional datasets

#### Dataset imdb ratings over time 

In order to understand how the ratings of certain movies has evolved over time, we used an the API provided by [WaybackMachine](https://archive.org/help/wayback_api.php) to get a snapshot of the [IMBD.com](https://www.imdb.com/) page of each movie one year and five years after the release. In this way we were able to obtain the rating and the number of people who voted, while associating them with the IMBD identifier provided in the [IMDB database](https://datasets.imdbws.com/title.basics.tsv.gz) and with the original dataset through the name of the movie.

## Methods

### Evolution movie plots and plot similarity
#### Plot preprocessing
First we filter out all movies with plots with less than 200 words. Then we use the NLTK library to tokenize the plots, filter out stopwords, lowercasing and stemming. We also filter out people's names. We then use the Bag-Of-Words model to represent the plots. We then use the gensim library to perform Latent Dirichlet Allocation (LDA). The LDA gives us the topics (we pick the amount) as a distribution over words, and for each movie plot how it is distributed over the topics. We can easily interpret the topics by looking at the most frequent words.

#### Evolution movie plots

To see how movie plots evolved over time, we use three approaches: 
- **First approach**: We start by doing a tf-idf transformation on the Bag Of Words vectors. We use PCA to reduce the dimensionality. We then perform k-means clustering to get a certain amount of clusters over the movie plots. We can interpret each cluster by taking a sample of the movies in them. Then for each time period (e.g. decade), we look how the movies in that time period are distributed over the clusters to get a sense of the type of movie plots in that time period.
- **Second approach**: We use the topic based representation generated by LDA. We can then again perform k-means clustering using this representation, interpreting each cluster by its centroid (e.g. a centroid could be: 40% war, 20% money, 40% other topics). We can then again see for each time period, how the movies were distributed over the clusters (optionally weighting each movie by its box office revenue as a proxy for its popularity).
- **Third approach**: Here we do a sentence by sentence sentiment analysis of each plot, to get a representation for its emotional arc. For each year, we then compute an average of this emotional arc for all the plots in each year. We can then see how the average emotional arc of movies changed over time.

### Plot complexity

To assess the complexity of a movie, we have used the following methodologies:

Assess plot summary length; longer summaries suggest complexity. Use TF-IDF for unique words, indicating complexity with varied scores. Measure text coherence by analyzing semantic similarity between sentences using sentence embeddings (e.g., Sentence Transformers). Variations in cosine similarity scores indicate plot complexity and coherence.


### Plot similarity
After text preprocesing, plot similarity can be computed in two ways:
- **Cosine distance**: The bag of words obtained is reduced to the first 100 words, avoiding long plots being more prone to be more similar to other plots due to its increased number of words. Then, the cosine distance between two plots can be computed fairly.A cosine distance of 1 would mean the two movies are identical, and a value of 0 would represent no similarity at all.
- **LDA and clustering**: Computing cosine distance with the frequency vectors lacks some complexity and fails to capture generalized topics. Using LDA algorithm, broaded topics can be extrapolated and more real similarity can be captured. Furthermore, it makes it easier for a clustering analysis by topic. In this way,  a movie which belongs to a big cluster and the closer it is to the center of the cluster, the less original is a movie.
 

### Movie metadata preprocessing

Firstly we removed all the movies without movie_box_office_reveneue (attempts to find datasets with additional box_office_revenue weren’t successful). We extracted the year from all the dates. Then we merged the movie.metadata dataset with the imbd one. Finally, we extracted the features that were encoded in a dictionary (language, genre, country) and added them to the dataset with onehot encoding. 

### Movie aging
For this part, we will use the [dataset imdb ratings over time](#Dataset-imdb-ratings-over-time). We took the difference between the ratings for one and five years after release. This shows which movie became more or less popular over time. Then we regressed the metadata of the movies on the difference in ratings to determine which features have greater influence on the popularity of a movie over time. 

### Most influential feature for revenue over time

Finally, to answer the question of which features had a higher influence on the revenue through the years we grouped by decades. Then we regressed over the revenue in each of these groups and sorted the coefficient to understand which were the more relevant features in each year group. 

## Timeline and organization

### Executed timeline

Steps ...: **Deadline Milestone 2 17.11.2022**

*01.12.2022: Deadline Homework 2*

*18.12.2022: complete notebook and start writing the blog*

Step ...: **Deadline Milestone 3 23.12.2022**

### Organization within the team

<table class="tg" style="table-layout: fixed; width: 342px">
<colgroup>
<col style="width: 16px">
<col style="width: 180px">
</colgroup>
<thead>
  <tr>
    <th class="tg-0lax">Teammate</th>
    <th class="tg-0lax">Contributions</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax">Oriol </td>
    <td class="tg-0lax">Plot similarity</td>
   <td class="tg-0lax">Analyze evolution of emotional arc</td>
  </tr>
  <tr>
    <td class="tg-0lax">Stefano V </td>
    <td class="tg-0lax">Finsh scraping of imdb ratings</td>
    <td class="tg-0lax">Regress on newly scraped ratings</td>
  </tr>
  <tr>
    <td class="tg-0lax">Stefano C</td>
    <td class="tg-0lax">Plot complexity</td>
  </tr>
  <tr>
    <td class="tg-0lax">Max</td>
    <td class="tg-0lax">Fully implement LDA</td>
    <td class="tg-0lax">Perform basic K-means clustering on bag-of-words vectors</td>
    <td class="tg-0lax">Analyze movies plot evolution using K-means clustering</td>
    <td class="tg-0lax">Analyze movies plot evolution using topic-based representation generated by LDA</td>

  </tr>
  <tr>
    <td class="tg-0lax">Michelle</td>
    <td class="tg-0lax">Exploratory Data Analysis</td>
    <td class="tg-0lax">Regress on groups of ten years</td>
  </tr>
</tbody>
</table>
