from pymongo import MongoClient
from bson.objectid import ObjectId
import feedparser
import time
from threading import Thread
from threading import Timer
from datetime import datetime
from time import mktime
import socket
from  classifier import Classifier
from bs4 import BeautifulSoup
from Queue import Queue
import threadpool

class Subscriber():
	def __init__(self, pool_size=10):
		socket.setdefaulttimeout(3)
		self.pool =threadpool.ThreadPool(pool_size) 
		self.documents = MongoClient().rss.documents
		self.classifier	= Classifier()

	def consume(self,line):		
		try:
			feeder = feedparser.parse(line)		
			if 'title' in feeder.feed.keys():
				site_title = feeder.feed['title']
			else:			
				site_title =u"No title found"		
			for entry in feeder.entries:			
				doc = {'site_url': line,'site_title': unicode(site_title)}						
				for item in ['title', 'link','summary','content','published_parsed','tags','author','summary_detail']:
					if item in entry.keys():
						doc[item] =entry[item]

				doc['published_parsed']=datetime.fromtimestamp(mktime(doc['published_parsed']))

				if 'content' not in doc.keys():
					doc['content'] = doc['summary']
				else:
					doc['content'] = doc['content'][0]['value']			
				print doc['title'].encode('utf8')
				
				if self.documents.find({'link':doc['link']}).count() == 0:			
					try:
						doc['category'] = self.classifier.predict(BeautifulSoup(doc['content']).text)
						print doc['category']
					except Exception, e:
						print e
					self.documents.insert(doc)
					print doc['title'].encode('utf8')						
		except Exception, e:			
			print e	

	def subscribe(self):		
		lines = [line.strip() for line in open('sites.txt','r')]		
		requests = threadpool.makeRequests(self.consume,lines, None) 
		for req in requests:
			self.pool.putRequest(req)
		self.pool.wait()

if __name__ == '__main__':
	subscriber = Subscriber(pool_size=30)
	while True:
		subscriber.subscribe()
		print 'wait...'
		time.sleep(10)
