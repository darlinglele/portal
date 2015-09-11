import jieba
import scipy
import os
import numpy as np
from scipy import sparse
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from pymongo import MongoClient
from bson.objectid import ObjectId
from time import time
from sklearn.neighbors import NearestNeighbors

STOP_WORDS = set(line.strip().decode('utf-8') for line in open("stopwords.dic", 'r'))

def tokenize(text):
        seg_list = jieba.cut(text, cut_all=False)
        return [x.strip() for x in seg_list if len(x.strip()) > 0 and x not in STOP_WORDS]

def get_rss_data():
    client = MongoClient()
    documents = client.rss.documents
    data = []
    ids = []
    for item in documents.find().sort('_id', 1).limit(1000):
        content = BeautifulSoup(item['content']).text
        data.append(content)
        ids.append(item['_id'])
    return data, ids
    

def get_notes_data():    
    client = MongoClient()
    notes = client.rss.notes
    data, ids = [],[]
    for item in notes.find().sort('_id', 1).limit(1000):        
        content = BeautifulSoup(item['content']).text
        data.append(content)
        ids.append(item['_id'])
    return data, ids


def key_words(data):
    vectorizer = TfidfVectorizer(tokenizer =tokenize)
    data = vectorizer.fit_transform(data)
    b = []
    cx = scipy.sparse.coo_matrix(data)
    for x in range(data.shape[0]):
        a = [(index, val)
             for index, val in zip(cx.getrow(x).indices, cx.getrow(x).data)]
        a = [x[0] for x in sorted(a, key=lambda x: x[1], reverse=True)]
        b.append(a[0:4])
    feature_names = vectorizer.get_feature_names()
    for i, x in enumerate(b):
        for j, y in enumerate(x):
            b[i][j] = feature_names[y]
    return b


def update_documents_key_words():
    data, doc_ids = get_rss_data()
    for index, names in enumerate(key_words(data)):
        doc_ids[index] = (doc_ids[index], names)

    client = MongoClient()
    documents = client.rss.documents
    for doc in doc_ids:
        documents.update(
            {'_id': ObjectId(doc[0])}, {'$set': {'keywords': doc[1]}})


def update_notes_key_words():
    data, doc_ids = get_notes_data()
    for index, names in enumerate(key_words(data)):
        doc_ids[index] = (doc_ids[index], names)

    client = MongoClient()
    notes = client.rss.notes

    for doc in doc_ids:
        print str(doc[0])
        notes.update({'_id': str(doc[0])}, {'$set': {'keywords': doc[1]}})

    tags = {}

    for doc in doc_ids:
        for key_word in doc[1]:
            tags.setdefault(key_word.strip(), 0)
            tags[key_word.strip()] += 1
    summary = client.rss.summary
    summary.update({'name': 'tags'}, {'$set': {'value': tags}})


def similiar():
    data, ids =get_notes_data()
    vector  = CountVectorizer(tokenizer=tokenize)
    X = vector.fit_transform(data)

    nbrs = NearestNeighbors(n_neighbors=5, algorithm='kd_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)
    print distances,indices
    # [[id,1,2],[id,2,3]]
    print type(indices)
    for i in  xrange(len(indices)):
        for j in xrange(len(indices[0])):
            indices[i][j] = ids[indices[i][j]]
    client = MongoClient()
    notes = client.rss.notes
    print indices
    for x in indices:
        notes.update({'_id': str(x[0])},{'$set': {'related':[str(i) for i in x[1:]]}})
        


if __name__ == '__main__':
    update_notes_key_words()	
    similiar()

