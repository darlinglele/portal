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

STOP_WORDS = set(line.strip() for line in open("stopwords.dic", 'r'))

def tokenize(text):
        seg_list = jieba.cut(text, cut_all=False)
        return [x for x in seg_list if x.encode('utf-8') not in STOP_WORDS]

def get_rss_data():
    start = time()
    client = MongoClient()
    documents = client.rss.documents
    data = []
    doc_ids = []
    for item in documents.find().sort('_id', 1).limit(1000):
        doc_ids.append(item['_id'])
        content = BeautifulSoup(item['content'].encode('utf-8')).text
        seg_list = tokenize(content)
        data.append(u' '.join(seg_list))
    print len(data), 'data loaded...:', time() - start
    return (data, doc_ids)

def get_nodes_data():    
    client = MongoClient()
    notes = client.rss.notes
    data, ids = []
    for item in notes.find().sort('_id', 1).limit(1000):
        content = BeautifulSoup(item['content']).text
        data.append(content)
        ids.append(item['_id'])
    return data, ids


def key_words(data):
    vectorizer = TfidfVectorizer(tokenier =tokenize)
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




if __name__ == '__main__':
    update_notes_key_words()
	# client = MongoClient()
	# notes = client.rss.notes	
	# for x in notes.find({'$or':[{'_id':{'$type' : 1}},{'status':'draft'}]}):    

    # vector  = CountVectorizer(tokenier=tokenize)
    # print vector.fit_transform() 