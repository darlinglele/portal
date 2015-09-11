from pymongo import MongoClient
import feedparser
import time

def pull_subscription():
	lines = [line.strip() for line in open('sites.txt')]	
	client = MongoClient()
	rss = client.rss
	documents =rss.documents
	for line in lines:				
		feeder = feedparser.parse(line)		
		site_title = feeder.feed.title		
		for entry in feeder.entries:
			doc = {'site_url': line,'site_title': unicode(feeder.feed.title)}
			for x in entry.keys():
				doc[x] = unicode(entry[x])			
			if documents.find({'link':doc['link']}).count() == 0:			
				documents.insert(doc)	

while True:	
	print "updating......"
	# pull_subscription()
	print "updated"
	break
	time.sleep(100)

def get_all_sites():
	site_urls = [line.strip() for line in open('sites.txt')]	
	client = MongoClient()
	rss = client.rss
	documents =rss.documents
	site_titles=[documents.find_one({'site_url': site_url})['site_title'] for site_url in site_urls]
	print site_titles
