import urllib2
import feedparser

urllist = [[line.split("%%%%")[0],line.split("%%%%")[1]] for line in open('feed','r')]
del urllist[0]
for url in urllist:
	print url[1]
	try:			
		response = urllib2.urlopen(url[1],timeout=1)
		localFile = open('./pages/'+url[0], 'w')
		html=response.read()
		print html
		localFile.write(html)
		localFile.close()
	except Exception, e:
		print e
