#encoding=utf-8   
import jieba   
import os
import numpy as np
from scipy import sparse
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
FEATURE_MATRIX=None
def get_data(dir):		
	data =[]
	for path in os.listdir(dir):
		content = BeautifulSoup(open(dir+path)).text			
		seg_list = jieba.cut(content,cut_all=False)
		data.append(u' '.join(seg_list))
	return data	

def extract_features(data):	
	vectorizer = HashingVectorizer(token_pattern='(?u)\\b\\w\\w+\\b')
	tfidfTransformer = TfidfTransformer()
	return tfidfTransformer.fit_transform(vectorizer.fit_transform(data))		

def get_nearest(dir,name):
	items =[file for file in os.listdir(dir)]
	global FEATURE_MATRIX	
	if FEATURE_MATRIX ==None or FEATURE_MATRIX.shape[0] < len(items):
		FEATURE_MATRIX = extract_features(get_data(dir))			
	nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(FEATURE_MATRIX)
	distances,indices = nbrs.kneighbors(FEATURE_MATRIX)
	index = indices[items.index(name)]
	nearests = [items[x] for x in index] 
	del nearests[0]
	return nearests
