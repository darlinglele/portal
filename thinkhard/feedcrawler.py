#encoding=utf8
import time
from datetime import datetime
from time import mktime
import socket
import feedparser
import threadpool

class FeedCrawler():
	def __init__(self,task):
		socket.setdefaulttimeout(task['timeout'])
		self.pool =threadpool.ThreadPool(task['pool_size']) 
		self.sources = task['sources']
		self.feeds = []
	
	def request(self,source):
		try:
			feeder = feedparser.parse(source)		
			if 'title' in feeder.feed.keys():
				site_title = feeder.feed['title']
			else:			
				site_title =u"No title found"		
			for entry in feeder.entries:			
				feed = {'site_url': source,'site_title': unicode(site_title)}						
				for item in ['title', 'link','summary','content','published_parsed','tags','author','summary_detail']:
					if item in entry.keys():
						feed[item] =entry[item]

				feed['published_parsed']=datetime.fromtimestamp(mktime(feed['published_parsed']))

				if 'content' not in feed.keys():
					feed['content'] = feed['summary']
				else:
					feed['content'] = feed['content'][0]['value']
				self.feeds.append(feed)
		except Exception, e:			
			print e	

	def crawl(self):					
		requests = threadpool.makeRequests(self.request,self.sources, None)
		for req in requests:
			self.pool.putRequest(req)
		self.pool.wait()
		self.pool.wait()
		return self.feeds



