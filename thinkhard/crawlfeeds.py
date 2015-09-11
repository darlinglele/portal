#encoding=utf8
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup
from feedcrawler  import FeedCrawler
from classification.naivebayesclassifier import NaiveBayesClassifier
import jieba
import re
import time


if __name__ == '__main__':	
    while True:
        print 'grap rss...'
        STOP_WORDS = set(line.strip().decode('utf-8') for line in open("stopwords.dic", 'r'))
        docs = MongoClient().rss.documents
        task={'timeout':5, 'pool_size':10, 'sources':[line.strip() for line in open('sites.txt')]}
        for doc in FeedCrawler(task).crawl():
            if docs.find({'link':doc['link']}).count() == 0:
                docs.insert(doc)
    		
    	    
        def tokenize(text):
            try:      
                # print text.encode('utf-8')      
                seg_list = jieba.cut(text, cut_all=False)
                zh_vocabulaly = re.compile(ur"([\u4E00-\u9FA5]+$)")                                    
                return [x.strip() for x in seg_list if zh_vocabulaly.match(x) and x not in STOP_WORDS]
            except Exception, e:
                print e
                return []
        client = MongoClient()
        documents = client.rss.documents
        print 'update category...'
        classifier = NaiveBayesClassifier(tokenizer=tokenize)    
        classifier.load(u'classification/classifier.dat')    
        classifier.reduce(max_size=404)
        for x in documents.find({},{'_id':'1','content':1}):
            content = BeautifulSoup(x['content']).text.encode('utf-8')
            category = classifier.predict(content)
            print category.encode('utf-8')
            documents.update({'_id': x['_id']},{'$set': {'category':category}})
    	time.sleep(1000)

