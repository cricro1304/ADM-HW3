import pandas as pd
import numpy as np
import nltk
import pickle
from ast import literal_eval
import math
import heapq


import functions
from functions import preprocess_query,search_engine_1,search_engine_part3

#import the data frame, the vocabulary, the inverted_index and the tfidf inverted_index
#df = pd.read_csv(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\df.csv")
#list_of_words = pd.read_csv(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\df_list_of_words.csv")
#with open(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\vocabulary.pkl", 'rb') as file:
#    vocabulary = pickle.load(file)
#with open(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\inverted_index.pkl", 'rb') as file:
#    inverted_index = pickle.load(file)
#with open(r"C:\Users\kkfam\Desktop\DATA_SCIENCE\ADM\HOMEWORKS\HOMEWORK_3\new_inverted_index.pkl", 'rb') as file:
#    tfidf_inverted_index = pickle.load(file)    #now this is the tfidf inverted index


    
## Since the min-heap is the python default, we implement a max-heap with the following function

def create_max_heap_from_dict(data):
    negated_data = [(-value, key) for key, value in data.items()]
    heapq.heapify(negated_data)
    return negated_data




def search_engine_2(df, vocabulary, inverted_index, tfidf_inverted_index, top_k = 5):
    '''
    The function computes the (fast) cosine similarity for each pair (query,document) and returns the top k according to this score.
    Reference for the fast cosine similarity:  "An introduction to Information Retrieval" by D. Manning, Raghavan, Schütze, Chp. 7

    :param df: the original dataframe
    :param vocabulary: the dictionary that maps terms in term_id
    :param inverted_index:
    :param tfidf_inverted_index: the complete dictionary with as keys the term_id and as values a list of tuples (doc_id, tfidf)
    :param top_k: the number of doc the function will retrieve. Default value = 5
    :return: a dataframe with the top k docs according to the (fast) cosine similarity score
             and the dictionary with the doc_id as keys and score similarity as values

    '''
    conjunctive_df, query = search_engine_1(df, inverted_index, vocabulary)
    list_query_term = preprocess_query(query)
    conjunctive_idx = conjunctive_df.index
    conjunctive_doc_list_descriptions = df.loc[conjunctive_idx, 'list_of_words']

    similarity_scores = {}

    # We loop through each doc_id that contains all the query terms
    for doc_idx in conjunctive_doc_list_descriptions.index:
        list_doc_term = conjunctive_doc_list_descriptions.loc[doc_idx]

        score = 0  # initialize the score function of the doc
        norm2_doc = 0  # initialize the norm2 of the doc
        norm2_query = len(
            list_query_term)  # the query vector has (formally) 1's at each query_term position and 0 otherwise
        norm2_query = math.sqrt(norm2_query)

        term_already_encountered = []  # Keep track of term already encountered in the list_doc_term
        for term in list_doc_term:

            term_id = vocabulary[term]

            # Retrieve TF-IDF values list for the given term_id
            tfidf_values = tfidf_inverted_index[term_id]

            # Search for the specific tuple with the given doc_id
            target_tuple = next((tup for tup in tfidf_values if tup[0] == doc_idx), None)

            if target_tuple:
                # If the tuple is found, retrieve the TF-IDF score (second element of the tuple)
                tfidf_score = target_tuple[1]
            else:
                print(f"{term} NOT FOUND")
                # Set tfidf_score to 0 if the term is not found in the document
                tfidf_score = 0

            norm2_doc += tfidf_score ** 2

            # If the term is in the query and we didn't count it already, we update the numerator
            if term in list_query_term and term not in term_already_encountered:
                term_already_encountered.append(term)
                score += tfidf_score

        norm2_doc = math.sqrt(norm2_doc)

        similarity_scores[doc_idx] = score / (norm2_doc * norm2_query)

    # Extract the top k doc
    # Sort the dictionary keys by their values in descending order
    sorted_keys = sorted(similarity_scores, key=similarity_scores.get, reverse=True)

    # Create a new dictionary using the sorted keys and values
    sorted_similarity_scores = {k: similarity_scores[k] for k in sorted_keys}

    # Extract the top k docs if number of docs > k
    if len(sorted_similarity_scores):
        sorted_similarity_scores = dict(list(sorted_similarity_scores.items())[:top_k])
    
    # Store the top_k documents in a max-heap structure
    topk_heap = create_max_heap_from_dict(sorted_similarity_scores)
    
    # Retrieve the corresponding dataframe of the documents
    top_idx = list(sorted_similarity_scores.keys())
    topk_df = conjunctive_df.loc[top_idx].copy()
    topk_df['Similarity'] = topk_df.index.map(sorted_similarity_scores.get)
    topk_df = topk_df.sort_values(by='Similarity', ascending=False)
    return topk_df,topk_heap




# a modified search_engine 2 for Part 3 that doesn't take the top_k and returns also other columns
def search_engine_2_part3(df, vocabulary, inverted_index, tfidf_inverted_index):
    '''
    The function computes the (fast) cosine similarity for each pair (query,document) and returns the top k according to this score.
    Reference for the fast cosine similarity:  "An introduction to Information Retrieval" by D. Manning, Raghavan, Schütze, Chp. 7

    :param df: the original dataframe
    :param vocabulary: the dictionary that maps terms in term_id
    :param inverted_index:
    :param tfidf_inverted_index: the complete dictionary with as keys the term_id and as values a list of tuples (doc_id, tfidf)
    :param top_k: the number of doc the function will retrieve. Default value = 5
    :return: a dataframe with the filtered docs(according to conjunctive query) and the corresponding similarity score

    '''
    conjunctive_df, query = search_engine_part3(df, inverted_index, vocabulary)
    list_query_term = preprocess_query(query)
    conjunctive_idx = conjunctive_df.index
    conjunctive_doc_list_descriptions = df.loc[conjunctive_idx, 'list_of_words']

    similarity_scores = {}

    # We loop through each doc_id that contains all the query terms
    for doc_idx in conjunctive_doc_list_descriptions.index:
        list_doc_term = conjunctive_doc_list_descriptions.loc[doc_idx]

        score = 0  # initialize the score function of the doc
        norm2_doc = 0  # initialize the norm2 of the doc
        norm2_query = len(
            list_query_term)  # the query vector has (formally) 1's at each query_term position and 0 otherwise
        norm2_query = math.sqrt(norm2_query)

        term_already_encountered = []  # Keep track of term already encountered in the list_doc_term
        for term in list_doc_term:

            term_id = vocabulary[term]

            # Retrieve TF-IDF values list for the given term_id
            tfidf_values = tfidf_inverted_index[term_id]

            # Search for the specific tuple with the given doc_id
            target_tuple = next((tup for tup in tfidf_values if tup[0] == doc_idx), None)

            if target_tuple:
                # If the tuple is found, retrieve the TF-IDF score (second element of the tuple)
                tfidf_score = target_tuple[1]
            else:
                print(f"{term} NOT FOUND")
                # Set tfidf_score to 0 if the term is not found in the document
                tfidf_score = 0

            norm2_doc += tfidf_score ** 2

            # If the term is in the query and we didn't count it already, we update the numerator
            if term in list_query_term and term not in term_already_encountered:
                term_already_encountered.append(term)
                score += tfidf_score

        norm2_doc = math.sqrt(norm2_doc)

        similarity_scores[doc_idx] = score / (norm2_doc * norm2_query)

    # Extract the top k doc
    # Sort the dictionary keys by their values in descending order
    #sorted_keys = sorted(similarity_scores, key=similarity_scores.get, reverse=True)

    # Create a new dictionary using the sorted keys and values
    #sorted_similarity_scores = {k: similarity_scores[k] for k in sorted_keys}

    # Extract the top k docs if number of docs > k
    #if len(sorted_similarity_scores):
    #    sorted_similarity_scores = dict(list(sorted_similarity_scores.items())[:top_k])
    
    # Store the top_k documents in a max-heap structure
    #topk_heap = create_max_heap_from_dict(sorted_similarity_scores)
    
    # Retrieve the corresponding dataframe of the documents
    filtered_df_idx = list(similarity_scores.keys())
    filtered_df = conjunctive_df.loc[filtered_df_idx].copy()
    filtered_df['Similarity'] = filtered_df.index.map(similarity_scores.get)
    filtered_df = filtered_df.sort_values(by='Similarity', ascending=False)
    return filtered_df