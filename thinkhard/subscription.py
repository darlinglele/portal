from pymongo import MongoClient
from bson.objectid import ObjectId
import feedparser
import time
from threading import Thread
from threading import Timer
import thread

SUBSCRIBE_THREAD = None


def start():
	global SUBSCRIBE_THREAD	
	if SUBSCRIBE_THREAD == None or SUBSCRIBE_THREAD.is_alive() is False:
		print 'create subscription job...'
		SUBSCRIBE_THREAD = Thread(target=subscribe, args=())
		SUBSCRIBE_THREAD.start()				

def stop():
	if SUBSCRIBE_THREAD!= None and SUBSCRIBE_THREAD.is_alive():
		try:
			SUBSCRIBE_THREAD._Thread__stop()
		except Exception, e:
			print e

def get_all_items():
	site_urls = [line.strip() for line in open('thinkhard/sites.txt')]		
	client = MongoClient()
	documents =client.rss.documents
	sites = []
	for index, site_url in enumerate(site_urls):
		document = documents.find_one({'site_url': site_url})
		if document!=None:			
			sites.append({'id':index, 'title': document['site_title'],'url': site_url})
	for site in sites:
		site['items'] = list(documents.find({'site_url': site['url']}).sort('published_parsed',-1))				
	return list(sites)

def get_all_sites():
	site_urls = [line.strip() for line in open('thinkhard/sites.txt')]		
	client = MongoClient()
	documents =client.rss.documents
	sites = []
	for index, site_url in enumerate(site_urls):
		document = documents.find_one({'site_url': site_url})
		if document!=None:			
			sites.append({'id':index, 'title': document['site_title'],'url': site_url})
	return sites		

def get_latest_items(size):
	client = MongoClient()
	documents =client.rss.documents
	return list(documents.find({}).sort([('_id',-1),('published_parsed',-1)]).limit(size))

def get_document(id):
	client = MongoClient()
	documents =client.rss.documents
	doc = documents.find_one({'_id': ObjectId(id)})
	return doc

def get_cates():
	client = MongoClient()
	documents =client.rss.documents	
	func='''
                function(obj,prev) 
                { 
                    prev.count++; 
                } 
        '''  

	return	documents.group({"category":1},{},{"count": 0},func)

def set_as_read(id):
	client =MongoClient()
	documents = client.rss.documents
	documents.update({'_id':ObjectId(id)},{'$set':{'read':1}})

def star(id):
	client =MongoClient()
	doc = client.rss.documents.find_one({'_id':ObjectId(id)})
	if 'star' in doc.keys():
		star = -(doc['star'] -1 )
		client.rss.documents.update({'_id':ObjectId(id)},{'$set':{'star': star}})
	else:
		client.rss.documents.update({'_id':ObjectId(id)},{'$set':{'star': 1}})
