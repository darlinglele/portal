import urllib2
import feedparser
import sqlite3
import fetchfeed
from threading import Thread
from threading import Timer

def download():

	print 'begin'
	conn = sqlite3.connect("./data.db")
	c = conn.cursor()
	fetchfeed.fetch_url()
	rows= c.execute('select id, url, status, content from documents where status= ? limit 0,100', (0,)).fetchall()
	task_lst = [{ name: row[i] for i , name in enumerate(list(('id','url','status','content')))} for row in rows]
	print '...'
	def update(task):
		try:					
			req =  urllib2.Request(task['url'],headers = {'User-Agent': 'Chrome'})
			response = urllib2.urlopen(req,timeout=3)		
			task['status'] = 1
			task['content'] =response.read().decode('utf-8')
			
			print str(task['id'])+ '...ok'	
		except Exception, e:
			print str(task['id'])+ task['url']
			print e 


	def get_status_content_id(task): 
		return [task['status'], task['content'],task['id']]

	for task in task_lst:
		e = Thread(target=update, args=(task,))
		e.start()
		e.join()

	c.executemany('update documents set status=?, content=? where id=?', map(get_status_content_id, task_lst))
	conn.commit()
	conn.close()
	print 'close'
	Timer(5, download).start()
download()

