#encoding=utf-8
from pymongo import MongoClient
from bson.objectid import ObjectId
import jieba
from bs4 import BeautifulSoup
from classification.naivebayesclassifier import NaiveBayesClassifier
from classification.weighter.informationgain import InformationGain




if __name__ == '__main__':
	client =MongoClient()
	# classifier = NaiveBayesClassifier(cutter=jieba)
	# classifier.load('classification/raw_features.dat')
	# classifier.reduce(max_size=450, weighter=InformationGain)
	documents = client.rss.documents
	# for x in documents.find({},{'_id':'0','content':1}):
	# 	category = classifier.predict_text(BeautifulSoup(x['content']).text)
	# 	print category
	# 	documents.update({'_id': x['_id']},{'$set': {'category':category}})
	#

 
	func='''
                function(obj,prev) 
                { 
                    prev.count++; 
                } 
        '''  

	print	documents.group({"category":1},{},{"count": 0},func)