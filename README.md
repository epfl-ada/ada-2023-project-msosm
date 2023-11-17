# Film Metamorphosis: from silent to ....?

## Abstract

Our research aim 
Since the inception of cinema in the late nineteenth century, movies have undergone a remarkable metamorphosis, evolving from silent, black-and-white motion pictures to the vibrant, immersive and captivating films of today. 

Technological advancements have played an essential role in shaping the cinematic landscape. The transition from silent films to the sound and color film revolutionized the aesthetics of these compositions. The introduction of digital technology further transformed the industry through super-realistic special effects and computer-generated imagery(CGI).

In the present era, the ease of movie consumption has reached unprecented heights thanks to digital platforms and streaming services. While this accessibility has undeniably expanded the quantity of available content, there is an unhindered countereffect such a potential trade-off in quality. The increased pressure on filmmakers to produce mass appeal and palatable content may have a negative impact on artistic standards.



## Research questions
This project aims to investigate on the above stated topic. With this goal in mind, some questions have been proposed to help us understand how movies have changed through time. The following interrogations will be answered during the project:

- Did the complexity of movie dialogues decrease over time? Can we find a correlation between the increase in smartphone usage and the decrease in attention span? 
- Is it true that movies have become more similar in recent years? 
- Which movie characteristic makes it age more slowly and stay popular for longer?
- How did the average emotional arc of movies change over time? 
- How did the impact of each feature on revenue change over time? which feature became more or less relevant through the years? 


## Additional datasets

#### Dataset imdb ratings over time 

In order to understand how the ratings of certain movies has evolved over time, we used an the API provided by [WaybackMachine](https://archive.org/help/wayback_api.php) to get a snapshot of the [IMBD.com](https://www.imdb.com/) page of each movie one year and five years after the release. In this way we were able to obtain the rating and the number of people who voted, while associating them with the IMBD identifier provided in the [IMDB database](https://datasets.imdbws.com/title.basics.tsv.gz) and with the original dataset through the name of the movie.

<!-- imdb_ratings -->

## Methods

### Movie metadata preprocessing

Firstly we removed all the movies without movie_box_office_reveneue (attempts to find datasets with additional box_office_revenue weren’t successful). 
We then normalized the format of the date, while dropping the one which didn’t respect the %Y-%m-%d' format. 
We then merged the movie.metadata dataset with the imbd one (which contained imbd id for each movie). Finally we extracted the features which were encoded in a dictionary (language, genre, country) and added them to the dataset with onehot encoding. 

### Sentiment analysis 

### Plot complexity

### Plot similarity
When evaluating plot similarity the goal is to obtain a sense of how original or unique a movie is. The method we have come up with analysis the plot summary through NLP resulting in a vector of words contained in the plot. Therefore, cosine distance can be computed between vectors of words to obtain a sense of how similar this movies are. The further in average a movie is from the rest, the more original it is.

More concretely, the process starts by filtering out all movies with plots with less than 200 words, since we have considered that not enough information can be extracted from them. Then, plots are processed by removing all stopwords, tokenizing, lowercasing, eliminating people's name and normalizing all verbs to infinitive form. After this, frequency of words is computed and forming a vector of pairs ('word',frequency). This vector is limited to the 100 most common words, otherwise long plots would be more prone to be similar to others since having more words. Finally, the cosine distance between two movie vectors is computed. The more words with higher frequency the two vectors have in common the highest the cosine distance will be and therefore the more similar. A cosine distance of 1 would mean the two movies are identical, and a value of 0 would represent no similarity at all.

#### Future implementations
Some alternative and complementary ideas have been discussed amongst the members of the group. The proposed method lacks the capacity of verb generalization, for instance, it ignores the fact that "murder" and "kill" could be related to the same topic. Finding the latent topics in movie plots, we believe, would enhance the performance of cosine similarity since currently it does not capture synonym verbs as the same. Latent topics could be computed using Latent Dirilecht Allocation(LDA).

Additionally, it would be interesting to come up with some clustering method for visualization and further data comprehension. In this way, we could observe big clusters of movies representing stereotypical movies(f.e: romantic comedies, war films)or small clusters for films less common. The bigger the cluster and the more a point is close to the center of it the less original is a movie. Still the method to achieve this is a bit unclear to us.

### Movie aging

For this part we will use the [dataset imdb ratings over time](#Dataset-imdb-ratings-over-time). We took the difference between the ratings for one and five years after release. This shows which movie became more or less popular over time. Then we regressed the difference in ratings over different set of features and by looking at the coefficients we found the features which had greater influence on the aging of the movie. The set of features that we used are movie genre ect. 


## Timeline and organization

### Executed timeline

Steps ...: **Deadline Milestone 2 17.11.2022**

*01.12.2022: Deadline Homework 2*

Step ...: **Deadline Milestone 3 23.12.2022**

### Organization within team

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
  </tr>
  <tr>
    <td class="tg-0lax">Stefano V </td>
    <td class="tg-0lax">Movie aging</td>
  </tr>
  <tr>
    <td class="tg-0lax">Stefano C</td>
    <td class="tg-0lax">Plot complexity</td>
  </tr>
  <tr>
    <td class="tg-0lax">Max</td>
    <td class="tg-0lax">Sentiment analysis</td>
  </tr>
  <tr>
    <td class="tg-0lax">Michelle</td>
    <td class="tg-0lax">Exploratory Data Analysis</td>
  </tr>
</tbody>
</table>
