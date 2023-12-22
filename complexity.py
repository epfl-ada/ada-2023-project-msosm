import pandas as pd
import numpy as np
import string
import re
import nltk
from nltk.corpus import words
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



nltk.download('punkt')
nltk.download('words')

common_words_5000 = pd.read_excel('./data/wordFrequency.xlsx', sheet_name='4 forms (219k)')


def count_words(input_string):
    words = input_string.split()
    return len(words)


def lexic_preprocessing(text):
    '''
    input: text (string)
    output: dictionary of the most complex (not frequent) words in text, associated with their frequency,
        and a dictionary of all the words in text, associated with their frequency
    '''
    
    #nltk.download('punkt')
    #nltk.download('words')

    # Tokenize words
    # hard remove 5000 most common words, puntuation, and 's, 't, ...
    words_tokenized = word_tokenize(text.lower(), language='english')
    bow_initial = words_tokenized.copy()
    words_tokenized = list(filter(lambda token: token not in string.punctuation, words_tokenized))
    words_tokenized = list(filter(lambda token: token not in list(common_words_5000['word']), words_tokenized))
    #words_tokenized = [word for word in words_tokenized if word not in common_words_5000['word']]
    words_tokenized = [word for word in words_tokenized if not (re.match(r"'\w", word) or word in ['\'\'', '``'])]
    
    # initialize the PorterStemmer
    porter_stemmer = PorterStemmer()

    # apply stemming to each word in the text
    stemmed_words_complex = [porter_stemmer.stem(word) for word in words_tokenized]
    stemmed_words_original = [porter_stemmer.stem(word) for word in bow_initial]

    # compute the frequency of words in text
    freq_dist_text_complex = FreqDist(stemmed_words_complex)
    freq_dist_text_original = FreqDist(stemmed_words_original)

    return freq_dist_text_complex, freq_dist_text_original


def TTR_lexical_complexity_metric(bow_complex, bow_original):
    # TTR index (reference: 10.1016/j.sbspro.2013.10.668)
    t = len(bow_complex)
    n = len(bow_original)
    TTR = t/n
    return TTR


def mass_lexical_complexity_metric(bow_complex, bow_original):
    # mass (1966) index (reference: 10.1016/j.sbspro.2013.10.668)
    t = len(bow_complex)
    n = len(bow_original)
    M = (np.log(n)+np.log(t)) / (np.log(n)**2)
    return M


def lexical_complexity(text, metric):
    bow_complex, bow_original = lexic_preprocessing(text)
    if metric == 'TTR':
        complexity = TTR_lexical_complexity_metric(bow_complex, bow_original)
    elif metric == 'mass':
        complexity = mass_lexical_complexity_metric(bow_complex, bow_original)
    else:
        raise ValueError('The specified metric does not exist.')
    
    return complexity


