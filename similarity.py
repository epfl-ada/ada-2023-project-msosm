from math import sqrt

#####################################
#  COSINE SIMILARITY HELPERS        #
#####################################

def dot_product(v1, v2):
    print(set(v1)& set(v2))
    return sum(v1[key] * v2[key] for key in set(v1) & set(v2))

def magnitude(vector):
    return sqrt(sum(value**2 for value in vector.values()))

def cosine_similarity(v1, v2):
    # Compute only cosine similarity for the first most common words
    # Otherwise long plots have more probabilities to have similar words with other plots
    return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))
