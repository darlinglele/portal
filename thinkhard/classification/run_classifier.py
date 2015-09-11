# encoding=utf-8
from pymongo import MongoClient
from bson.objectid import ObjectId
import jieba
import re
from bs4 import BeautifulSoup
from naivebayesclassifier import NaiveBayesClassifier
from weighter.informationgain import InformationGain


if __name__ == '__main__':	
    STOP_WORDS = set(line.strip().decode('utf-8') for line in open("stopwords.dic", 'r'))
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
    classifier = NaiveBayesClassifier(tokenizer=tokenize)    
    classifier.load(u'raw_features_1.dat')    
    classifier.reduce(max_size=404, weighter=InformationGain)
    for x in documents.find({},{'_id':'1','content':1}):
        content = BeautifulSoup(x['content']).text.encode('utf-8')
        category = classifier.predict_text(content)
        print category.encode('utf-8')
        documents.update({'_id': x['_id']},{'$set': {'category':category}})
