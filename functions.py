import pandas as pd
import numpy as np
import nltk
import pickle
import math
from ast import literal_eval

#nltk library for tokenization, stemming and removing punctuation
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from nltk.stem import *
from nltk.corpus import stopwords

nltk.download('stopwords')
lst_stopwords = stopwords.words('english')
stemmer = PorterStemmer()





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


def build_df(df):
    #list_of_words = pd.read_csv(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\df_list_of_words.csv")
    list_of_words = pd.read_csv('df_list_of_words.csv')
    #Add a column to the df with the list of preprocessed query for each doc
    df['list_of_words'] = list_of_words
    #Convert the strings representing lists of terms to actual lists
    df['list_of_words'] = df['list_of_words'].apply(literal_eval)
    return df


# Function to update inverted index for each row
def update_inverted_index(row, inverted_index, vocabulary):
        
    document_id = row.name  # Get the document ID (DataFrame index)
    terms = row['list_of_words']
    for term in terms:
        term_id = vocabulary.get(term)
        if term_id is not None:
            if document_id not in inverted_index[term_id]:
                inverted_index[term_id].append(document_id)

                
def preprocess_query(query):
    '''
    
    :param query: the query string
    :return: a list with all the preprocessed term in the query
    
    '''
    # Preprocess the query
    tokenizer = RegexpTokenizer(r'\w+')
    #query = tokenizer.tokenize(query)
    query = ' '.join(tokenizer.tokenize(str(query))) if isinstance(query, str) else query
    stemmer = PorterStemmer()
    query = ' '.join([stemmer.stem(word) for word in str(query).split(' ') if not word in lst_stopwords])
    query = [word for word in query.split(' ')]
    
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



# a modified search_engine for part 3 that returns also other columns
def search_engine_part3(df, inverted_index, vocabulary):
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
    columns_to_select = ['courseName', 'universityName', 'courseDescription', 'url','score_fees','score_ranking','fees_eur','Ranking', 'city', 'country']
    doc_found = df.loc[list(conjunctive_list), columns_to_select].copy()
    return doc_found, query_string
