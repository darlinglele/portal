from pymongo import MongoClient
from bson.objectid import ObjectId
import feedparser
import time
from threading import Thread
from threading import Timer
import thread

SUBSCRIBE_THREAD = None

def subscribe():
	a ={'a':1}
	lines = [line.strip() for line in open('sites.txt')]	
	client = MongoClient()
	rss = client.rss
	documents =rss.documents
	for line in lines:				
		feeder = feedparser.parse(line)		
		if 'title' in feeder.feed.keys():
			site_title = feeder.feed['title']
		else:			
			site_title =u"No title found"
		for entry in feeder.entries:			
			doc = {'site_url': line,'site_title': unicode(site_title)}
			print entry.keys()
			for item in ['title', 'link','summary','content','published','tags','authors','summary_detail']:
				if item in entry.keys():
					doc[item] =entry[item]
			if 'content' not in doc.keys():
				doc['content'] = doc['summary']
			else:
				doc['content'] = doc['content'][0]['value']			
			# print  doc['content'].encode('utf8')
			if documents.find({'link':doc['link']}).count() == 0:			
				documents.insert(doc)				
	print 'waitting...'			
	# Timer(20, subscribe).start()			
subscribe()