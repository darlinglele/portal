import os
from pymongo import MongoClient
if __name__ == '__main__':
	cate= 'games'
	
	dir = 'data/'+cate+'/'	
	if not os.path.exists(dir):
		os.makedirs(dir)
	
	client = MongoClient()
	pages = client[cate].pages

	
	for i,x in enumerate(pages.find({'$where': 'this.content.length>400'})):
		f = open(dir+'/'+str(i),'w')
		f.write(x['content'].encode('utf8'))
		f.close()

		

	for root, dirs, files in os.walk('data/'+cate, True):    	
		for name in files:
			lines= open(os.path.join(root, name)).readlines()
			f= open(os.path.join(root,name),'w')
			for x in lines:
				if len(x)>100:
					f.write(x)	
					# print x
			f.close()	


	# # for x in open('data/ent/111'):
	# # 	print x + str(len(x))

