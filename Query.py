# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 20:02:40 2019

@author: Lenovo
"""

import pkuseg
import csv
import sys
import json
from gensim import corpora
from gensim import models
import numpy as np

def EnlargeField():
    maxInt = sys.maxsize
    decrement = True
    while decrement:
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt/10)
            decrement = True

def CreateQueryDictionary():
    tf_idf = models.TfidfModel.load("trained_tfidf")
# =============================================================================
#     with open('doc_token_file.txt','r',encoding='UTF-8') as doc_token_file:
#         reader = doc_token_file.readlines()
#         line_num = 0
#         for line in reader:
#             if line_num % 2 == 0:
#                 dictionary_ids.append(line[:-1])
#             else:
#                 words = line.split()
#                 dictionary_tokens.append(words)
#             line_num += 1
#             print(line_num)
# =============================================================================
            #if line_num > 201:
            #    break
    # print(dictionary_ids)
    # print(dictionary_tokens)
    dictionary = corpora.Dictionary(dictionary_tokens)
    token_id_dictionary.update(dictionary.token2id)
    i = 0
    for doc in dictionary_tokens:
#        numbered_word = dictionary.doc2bow(doc)
        words_idf = dict(tf_idf[numbered_words[i]])
        words_idf_dictionary.append(words_idf)
        i += 1
    print("QueryDictionary Created!")

def Query():
    seg = pkuseg.pkuseg()
    with open("stopwords-master/百度停用词表_Chinese.txt","r",encoding='UTF-8') as stopwords_file:
        reader = stopwords_file.readlines()
        for line in reader:
            stopwords.append(line[:-1])

    request = input("Request:")
    while request != '0' :
        query_tokens = seg.cut(request)     # 分词
        for token in query_tokens:          # 删去停用词
            if token in stopwords:
                query_tokens.remove(token)
        dimension = len(query_tokens)
        query_vector = np.ones(dimension)
        # 开始遍历文档，求每个文档的向量，并求余弦距离，放入字典中
        cosine_map = {}
        index = 0
        while index < len(dictionary_ids) :
            doc_vector = []
            for token in query_tokens:
                if token in token_id_dictionary:
                    token_id = token_id_dictionary[token]
                    if token_id in words_idf_dictionary[index].keys() :
                        token_tfidf = words_idf_dictionary[index][token_id]
                        # print(token_tfidf)
                        doc_vector.append(token_tfidf)
                    else:
                        doc_vector.append(0)
                else:
                    doc_vector.append(0)
            # doc_vector为doc的向量
            doc_vector = np.array(doc_vector)
            # 下面求余弦距离
            cosine = Cosine(query_vector,doc_vector)
            if cosine != 0:
                cosine_map[cosine] = dictionary_ids[index]
            index += 1
            print(index)
        # 对cosine字典按键反向排序
        cosine_sorted = sorted(cosine_map,reverse=True)
        print(cosine_sorted)
        # 打印前20个文档的id
        i = 0
        while i < 20:
            print(cosine_map[cosine_sorted[i]])
            i += 1
        
        request = input("Request:")

def Cosine(vector_a,vector_b):
    if np.all(vector_a == 0) or np.all(vector_b == 0):
        cos = 0
    else:
        mul = np.dot(vector_a,vector_b)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        cos = mul / denom
    return cos

def LoadDict():
    global dictionary_ids, dictionary_tokens, numbered_words
    with open("dictionary_ids",'r') as f:
        dictionary_ids = json.load(f)
    with open("dictionary_tokens",'r') as f:
        dictionary_tokens = json.load(f)
    with open("numbered_words",'r') as f:
        numbered_words = json.load(f)
    print("Load Done!")

EnlargeField()
stopwords = []
numbered_words = []
dictionaries = {}
dictionary_ids = []
dictionary_tokens = []
token_id_dictionary = {}
words_idf_dictionary = []
LoadDict()
CreateQueryDictionary()
Query()