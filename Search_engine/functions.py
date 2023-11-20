import pandas as pd
import numpy as np
import nltk
import pickle
import math

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



#Make the df exactly the same of the github example
def change_columns(df):
    df = df.drop(columns=['urls'])  # drop columns we don't need
    df = df.drop(df.columns[0], axis=1)
    df.rename(columns={'fullTime': 'isItFullTime'}, inplace=True)  # rename the columns with the github example names
    url_col = df.url  # change the col positions according to the github example (of course don't strictly needed, however...)
    df.drop(columns=['url'], inplace=True)
    df['url'] = url_col
    courses = df.courseName
    df['courseName'] = df['universityName']
    df['universityName'] = courses
    df.rename(columns={'courseName': 'universityName', 'universityName': 'courseName'}, inplace=True)
    faculties = df.facultyName
    df['facultyName'] = df['universityName']
    df['universityName'] = faculties
    df.rename(columns={'facultyName': 'universityName', 'universityName': 'facultyName'}, inplace=True)
    return df



def preprocess_query(query):
    '''
    
    :param query: the query string
    :return: a list with all the preprocessed term in the query
    
    '''
    # Preprocess the query
    tokenizer = RegexpTokenizer(r'\w+')
    query = tokenizer.tokenize(query)
    stemmer = PorterStemmer()
    query = [stemmer.stem(word) for word in query if not word in lst_stopwords]
    
    return query

def search_engine_1(df, inverted_index, vocabulary):
    '''
    :param df: the original dataframe
    :param inverted_index: it's a dictionary
    :param vocabulary: it's a dictionary
    :return: the dataframe with only the courses whose descriptions contain all the terms in the query
             and the query string (for practical reason)
    '''

    #Ask for the query
    query_string = input('Make a query: ')

    # Preprocess the query
    query = preprocess_query(query_string)
    
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
    return doc_found, query_string


## functions for part 2.2


def tfidf(df,inverted_index,vocabulary):
    '''

    :param df: the original dataframe
    :param inverted_index_vocabulary: the already existing dictionary with term_id and doc_id
    :return: the new tfidf_inverted_index
    '''
    tot_num_doc = len(df)  # Total number of documents

    # Initialize the new dictionary
    new_tfidf_dict = {}

    for term in vocabulary:
        term_id = vocabulary[term]
        list_of_doc = inverted_index[term_id]
        list_of_doc_id = list(set(list_of_doc))  # Remove duplicates

        term_tfidf_values = []
        for doc_id in list_of_doc_id:
            df_row = df.loc[doc_id, 'list_of_words']  # Getting the list courseDescription already preprocessed
            tf = df_row.count(term) / len(df_row)  # Compute the term frequency
            num_doc_containing_term = len(list_of_doc_id)
            idf = math.log(tot_num_doc / num_doc_containing_term)  # Compute the inverse doc frequency
            tfidf = tf * idf  # Compute the TF-IDF

            # Append tuple (doc_id, tfidf) to term's TF-IDF values list
            term_tfidf_values.append((doc_id, tfidf))

        # Assign term's TF-IDF values list to the term_id in the new dictionary
        new_tfidf_dict[term_id] = term_tfidf_values

    return new_tfidf_dict