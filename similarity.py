import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import spacy

from math import sqrt
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
ner = spacy.load("en_core_web_sm")
tokenizer = RegexpTokenizer(r'\w+')

#####################################
#  COSINE SIMILARITY HELPERS        #
#####################################

def dot_product(v1, v2):
    return sum(v1[key] * v2[key] for key in set(v1) & set(v2))

def magnitude(vector):
    return sqrt(sum(value**2 for value in vector.values()))

#####################################
#  TEXT PREPROCESSING HELPERS       #
#####################################

def is_name(word):
    # Named Entity Recognition for Person's Name
    doc = ner(word)
    for word in doc.ents:
        if word.label_ == "PERSON":
            return True
    return False

def is_verb(word):
    # Use WordNet to check if the word is a verb
    synsets = wordnet.synsets(word)
    for synset in synsets:
        if synset.pos() == 'v':
            return True
    return False

def get_infinitive_form(verb):
    lemmatizer = WordNetLemmatizer()
    infinitive_form = lemmatizer.lemmatize(verb, pos='v')
    return infinitive_form

#####################################
#  PUBLIC METHODS                   #
#####################################

def cosine_similarity(v1, v2):
    # Compute only cosine similarity for the first most common words
    # Otherwise long plots have more probabilities to have similar words with other plots
    v1 = dict(Counter(v1).most_common(100))
    v2 = dict(Counter(v2).most_common(100))
    return dot_product(v1, v2) / (magnitude(v1) * magnitude(v2))

def preprocess_text(text):
    # Tokenize the text and remove all punctuation
    words = tokenizer.tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    # Lowercase everything and filter out stopwords
    words = [word.lower() for word in words if word.lower() not in stop_words]

    # Sometimes people's name can also be verbs, therefore we should remove them first
    # For instance, to carol: to sing especially in a joyful manner
    # Also it may induce similarities which are not there. There are both Harry's in Harry Potter and Mamma Mia without having anything in common
    words = list(filter(lambda word: not is_name(word), words))
    
    # Separate verbs and others to obtain the infinitive form and be able to generalizes
    verbs = list(filter(is_verb, words))
    others = list(filter(lambda word: not is_verb(word), words))

    # Transform verbs into their infinitive form
    verbs = [get_infinitive_form(verb) for verb in verbs]

    # Count words appearance
    words = Counter(verbs + others)
    return dict(words)