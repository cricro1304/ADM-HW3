import pandas as pd
import numpy as np
import nltk
import pickle

#nltk library for tokenization, stemming and removing punctuation
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from nltk.stem import *
from nltk.corpus import stopwords

nltk.download('stopwords')
lst_stopwords = stopwords.words('english')
stemmer = PorterStemmer()

#import the data frame, the vocabulary and the inverted_index
df = pd.read_csv(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\df.csv")
list_of_words = pd.read_csv(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\df_list_of_words.csv")
with open(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\vocabulary.pkl", 'rb') as file:
    vocabulary = pickle.load(file)

with open(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\inverted_index.pkl", 'rb') as file:
    inverted_index = pickle.load(file)



def search_engine_1(df, inverted_index, vocabulary):
    '''

    :param df: the original dataframe
    :param inverted_index: it's a dictionary
    :param vocabulary: it's a dictionary
    :return: the dataframe with only the courses whose descriptions contain all the terms in the query
    '''

    query = input('Make a query: ')

    # Preprocess the query
    tokenizer = RegexpTokenizer(r'\w+')
    query = tokenizer.tokenize(query)
    stemmer = PorterStemmer()
    query = [stemmer.stem(word) for word in query if not word in lst_stopwords]

    conjunctive_list = inverted_index[vocabulary[query[0]]]  # initialize the conjunctive query list
    for term in query:
        if term in vocabulary:
            term_id = vocabulary[term]
            term_list = inverted_index[term_id]
            conjunctive_list = set(conjunctive_list).intersection(set(term_list))
        else:
            print("Not all terms are in the course's descriptions")
            return False
    columns_to_select = ['courseName', 'universityName', 'courseDescription', 'url']
    doc_found = df.loc[list(conjunctive_list), columns_to_select].copy()
    return doc_found

#preprocess it and transform it into a list