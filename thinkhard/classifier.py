#encoding=utf-8
import numpy
import heapq
import jieba
import logging
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from decimal import *
from time import time
from collections import Counter
import re
from math import log
STOPS = set(unicode(x.strip(),'utf-8') for x in open('stopwords.dic','r'))
logging.basicConfig(filename='log.txt',level=logging.INFO)

class Classifier(object):
	"""docstring for Classifier"""
	def __init__(self,encoding='GB18030'):
		self.terms_dic = None
		self.categories_dic= None
		self.doc_terms_cache=[0,1]
		client = MongoClient()
		self.terms = client.rss.terms
		self.doc_terms = client.rss.doc_terms
		self.categories = client.rss.categories
		self.selected_terms=None
		self.document_count=0.0
		self.encoding=encoding
		self.term_prob_cache={}
	def train(self,source):
		f.write('begin train....')
		self.terms_dic, self.categories_dic = self.__train(source) # print soup.text
		self.terms.remove()
		self.categories.remove()
		# print self.terms_dic
		# map_id_name = {"C000008" : "财经" , "C000010" : "IT" ,"C000013" : "健康" ,"C000014" : "体育" ,"C000016" : "旅游" ,"C000020" : "教育" ,"C000022" : "招聘","C000023" : "文化" ,"C000024" : "军事"}
		for key, value in self.terms_dic.iteritems():
			self.terms.insert({'_id': key,'document_count':value['document_count'],'total_count':value['total_count'],'category_count': value['category_count']})
		for key, value in self.categories_dic.iteritems():
			self.categories.insert({'_id': key,'name':key,'count': value})

	def extract(self,doc,text=None, encoding='GB18030'):
			print 'extract ', doc.encode('utf-8')
			try:
				content =text or open(doc).read().decode(encoding)
				seg_list = jieba.cut(content,cut_all=False)
				return [ x.strip() for x in set(seg_list) if len(x.strip()) >= 1 and x not in STOPS]
			except Exception, e:
				print e
				return []

	def get_row_terms(self,doc):
		doc_terms = self.doc_terms.find_one({'_id': doc})
		if doc_terms:
			return [x for x in doc_terms['terms'] if x in self.selected_terms]
		else:
			print 'split....'
			doc_terms = self.split(doc, encoding=self.encoding, distinct=True)
			if doc_terms:
				self.doc_terms.insert({"_id": doc,"terms":doc_terms})
			return [x for x in doc_terms if x in self.selected_terms]
		# return self.split(doc,distinct=True)

	def __train(self,dir,topdown=True):
		terms_dic = {}
		categories_dic = {}
		for root, dirs, files in os.walk(dir, topdown):
			for name in files:
				print root,name,'.....'
				category_id = root.split('/')[-1]
				term_count_dic = self.split(os.path.join(root,name),encoding=self.encoding)
				# print term_count_dic
				for term,count in term_count_dic.iteritems():
							terms_dic.setdefault(term,{})
							terms_dic[term].setdefault('total_count', 0)
							terms_dic[term].setdefault('category_count',{})
							terms_dic[term]['category_count'].setdefault(category_id,0)
							terms_dic[term]['total_count']+= count
							terms_dic[term]['category_count'][category_id]+=1
							terms_dic[term].setdefault('document_count',0)
							terms_dic[term]['document_count'] += 1
				categories_dic.setdefault(category_id,0)
				categories_dic[category_id] += 1

		return terms_dic, categories_dic


	def termprob(self,term, category_id):
		if categorycount(category_id) == 0: return 0
		return Decimal(self.__termcount(term,category_id))/Decimal(self.categories_dic[category_id])

	def categorycount(self,category_id):
		if category_id in self.categories_dic:
			return self.categories_dic[category_id]
		else:
			return 0

	def __termcount(self, term, category_id):
		if term in self.terms_dic and category_id in self.terms_dic[term]:
			return self.terms_dic[term][category_id]
		else:
			return 0
	def __weightedtermprob(self,term, category_id, weight = 1, alpha = 0.5):
		if term+category_id in self.term_prob_cache:
			return self.term_prob_cache[term+category_id]
		totals =0
		basictermprob=0
		if term in self.selected_terms:
			categories_count_dic=self.selected_terms[term]['category_count']
			totals = sum([x for x in categories_count_dic.itervalues()])
			if category_id in categories_count_dic:
				basictermprob = Decimal(categories_count_dic[category_id]) /Decimal(self.categorycount(category_id))

		bp = (Decimal(weight*alpha) + (totals*basictermprob)) / (weight+totals)
		self.term_prob_cache[term+ category_id] = bp
		return bp

	def __totalcount(self):
		return sum([x for x in self.categories_dic.itervalues()])

	def __docprob(self,doc, category_id):
		if self.doc_terms_cache[0] != doc:
			self.doc_terms_cache[0] = doc
			self.doc_terms_cache[1] = self.get_row_terms(doc)
		terms = self.doc_terms_cache[1]
		p =1
		star = time()
		for term in terms:
			p*= self.__weightedtermprob(term,category_id)
		# print time() - star
		return p

	def __textprob(self,text, category_id):
		terms = self.get_row_terms('..',text= text)
		p =1
		star = time()
		for term in terms:
			p*= self.__weightedtermprob(term,category_id)
		return p

	def __prob(self,doc, category_id):
		return self.__docprob(doc, category_id) * self.categorycount(category_id)/self.__totalcount()

	def doc_sort(self,doc):
		return sorted([(x, self.__prob(doc,x)) for x in self.categories_dic],key= lambda x: x[1], reverse=True)

	def text_sort(self,text):
		return sorted([(x, self.__textprob(text,x)) for x in self.categories_dic],key= lambda x: x[1], reverse=True)

	def load_terms_dic(self):
		return {x['_id']: {'total_count': x['total_count'],'document_count':x['document_count'], 'category_count': x['category_count']} for x in self.terms.find({'total_count':{'$gt':100}})}

	def load_categories_dic(self):
		return {x['_id']: x['count'] for x in self.categories.find()}

	def load_data(self):
		self.terms_dic = self.terms_dic or self.load_terms_dic()
		self.categories_dic = self.categories_dic or self.load_categories_dic()

	def test(self,source):
		f.write('begin test....')
		total_count =0
		error_count =0
		# self.select()
		for root, dirs, files in os.walk(source, topdown=True):
				for name in files:
					print root, name
					category_id = root.split('/')[-1]
					categories = self.doc_sort(os.path.join(root,name))
					total_count+=1
					if category_id not in [x[0] for x in categories[0:1]]:
						error_count+=1
						print categories,str((1 - Decimal(error_count)/Decimal(total_count))*100)
						# f.write('error....'+str(Decimal(error_count)/Decimal(total_count)))
		# f.close()
		return Decimal(error_count)/Decimal(total_count)

	def predict(self,text):
		self.load_data()
		return self.text_sort(text)[0][0]



	def get_row_terms(self,doc, text=None):
		if text is None:
			doc_terms = self.doc_terms.find_one({'_id': doc})
			if doc_terms:
				return [x for x in doc_terms['terms'] if x in self.selected_terms]
			else:
				print 'split....'
				doc_terms = self.split(doc, encoding=self.encoding,distinct=True)
				if doc_terms:
					self.doc_terms.insert({"_id": doc,"terms":doc_terms})
				return [x for x in doc_terms if x in self.selected_terms]
		else:
			return self.split(None, text=text, distinct=True)
		# return self.split(doc,distinct=True)

	def split(self,doc,text=None,encoding='GB18030', distinct=False):
			try:
				content =text or open(doc).read().decode(encoding)
				seg_list = jieba.cut(content,cut_all=False)
				zh_vocabulaly = re.compile(ur"([\u4E00-\u9FA5]+$)")
				term_lst = [x.strip() for x in seg_list if zh_vocabulaly.match(x) and  x not in STOPS]
				if distinct:
					return list(set(term_lst))
				counter = Counter(term_lst)
				terms_dic = {}
				for x in counter:
					terms_dic[x] = counter[x]
				return terms_dic
			except Exception, e:
				logging.info(str(e))
				return {}


	def select(self, min_df=2,dimension=10000,func=None, data={'terms':None,'categories':None}):
		print 'select terms ...'
		self.terms_dic = data['terms'] or {x['_id']: {'total_count': x['total_count'],'document_count':x['document_count'], 'category_count': x['category_count']} for x in self.terms.find({'document_count':{'$gt':min_df}})}
		self.categories_dic =data['categories'] or {x['_id']: x['count'] for x in self.categories.find()}
		self.document_count =sum([x for x in self.categories_dic.itervalues()])

		for x in self.terms_dic:
			self.terms_dic[x]['weight'] = self.ig(x)

		selected_terms = sorted([x for x in self.terms_dic.items()], key= lambda x: x[1]['weight'], reverse=True)[0:dimension]

		self.selected_terms = {x[0]: x[1] for x in selected_terms}
	def H(self):
		p_lst= [Decimal(x)/ self.document_count for x in self.categories_dic.itervalues()]
		return -sum([ x*Decimal(log(x,2)) for x in p_lst])

	def ig(self,t):
		return self.H() - self.H_T(t)
	def H_T(self,t):
		t_document_count = self.terms_dic[t]['document_count']
		_t_document_count = self.document_count - t_document_count
		pt= Decimal(t_document_count) / self.document_count
		p_t = 1-pt
		print t.encode('utf8'),'p(t)', pt
		print t.encode('utf8'),'p(_t)', p_t
		t_category_count = self.terms_dic[t]['category_count']
		#p(c|t)
		pt_c = [Decimal(x)/t_document_count for x in t_category_count.itervalues()]

		_t_category_count = []

		for category, count in self.categories_dic.items():
			t_count = t_category_count.get(category,0)
			_t_category_count.append(count - t_count)
		# p(Ci|_t)
		p_t_c = [Decimal(x)/ _t_document_count for x in _t_category_count]
		print t.encode('utf8'),'p(c|_t)',p_t_c
		print t.encode('utf8'),'p(c|t)',pt_c
		return -pt*sum([x*Decimal(log(x,2)) for x in pt_c if x !=0]) - p_t * sum([x*Decimal(log(x,2)) for x in p_t_c if x!= 0])

if __name__ == '__main__':

	classifier = Classifier(encoding='utf-8')
	classifier.select(20,600)
	for x in classifier.selected_terms:
		print x.encode('utf-8')
	# print classifier.selected_terms
	print classifier.test('data_test')
