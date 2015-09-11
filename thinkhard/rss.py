import sqlite3
import jieba
from bs4 import BeautifulSoup
import cluster

from time import time
from sklearn.cluster import KMeans, MiniBatchKMeans
import config
K = 20
SIZE =1000
INDICES=None

def rss_indices():
	conn = sqlite3.connect(config.DB)
	c = conn.cursor()
	rows= c.execute('select content from documents where status= ? limit 0,'+ str(SIZE), (1,)).fetchall()
	data = []
	start  = time()
	for row in rows:
		content = row[0]
		content = BeautifulSoup(content).text
		seg_list = jieba.cut(content,cut_all=False)
		data.append(u' '.join(seg_list)) 	
			

	print 'loading data cost ', time() - start

	feature_matrix = cluster.extract_features(data)

	km = KMeans(n_clusters=K, init='k-means++', max_iter=10000, n_init=1,
	                verbose=False)
	# km = MiniBatchKMeans(n_clusters=8, init='k-means++', n_init=1,
	                         # init_size=1000, batch_size=1000, verbose=False)
	km.fit(feature_matrix)	
	
	return km.labels_


def get_rss(): 
	global INDICES
	conn = sqlite3.connect(config.DB)
	c = conn.cursor() 
	rows= c.execute('select id, url, title from documents where status= ? limit 0,'+str(SIZE), (1,)).fetchall()
	lst = [{'id':row[0],'url': row[1],'title':row[2]} for row in rows]

	if INDICES == None or len(lst)!= INDICES.shape[0]:
		INDICES = rss_indices()
	outputs =[[] for x in range(K)]
	for i, j in zip(INDICES, lst):
		outputs[i].append(j)
	return outputs

get_rss()

