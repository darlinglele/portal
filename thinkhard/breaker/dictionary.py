# encoding=utf8
from array import array
from time import time
import jieba

trie1 = {
    '中': (0, {'国': (0, {'人': (0, None), '梦': (0, None)}), '央': (0, {'台': (1, None)})})}


def build(terms):
    trie = {}
    for term in terms:
        insert(term, trie)
    return trie


def insert(term, trie):
    if len(term) == 0:
        return trie
    if term[0] not in trie:
        trie[term[0]] = [len(term) == 1, insert(term[1:], {})]
    else:
        if len(term) == 1:
            trie[term[0]][0] = True
        trie[term[0]][1] = insert(term[1:], trie[term[0]][1])
    return trie


def search(trie, term):
    if len(term) <= 1:
        is_terminal = term in trie and trie[term][0]
        return (is_terminal, trie[term[0]][1] if term in trie else {})
    else:
        if term[0] in trie:
            return search(trie[term[0]][1], term[1:])
        else:
            return (False, {})


def cut(text, trie):
    begin = 0
    lst = []
    temp = None
    for i, x in enumerate(text):
        cur = text[begin:i + 1]        
        is_terminal, sub_trie = search(trie, cur)        
        if not is_terminal and len(sub_trie) == 0:
            lst.append(temp or cur)            
            begin += len(temp or cur)
            temp =None
                
        if is_terminal and len(sub_trie) > 0:
            temp = cur

        if is_terminal and len(sub_trie) == 0:
            lst.append(cur)
            temp = None
            begin = i + 1

    return lst

def cut2(text,term_set):
	last= len(text)-1
	lst =[]
	begin=0	
	count =0
	while begin <= last:			
		for x in xrange(5):
			cur = text[begin:begin+5-x]
			# print cur
			if cur in term_set:
				lst.append(cur)
				begin += len(cur) 
				# print cur
				break
		lst.append(text[begin:begin+1])					
		begin+=1

		count+=1	
	return lst	

# terms = ['abc', 'def', 'ab', 'ae', 'a']
# text = 'abc def ab ae  * abc'
# trie = build(terms)

# print cut(text, trie)


terms = ['abc', 'def', 'ab', 'eb', 'ae', 'a']
term_set =set(terms)
text = 'abc def ab ae  * abc '
print cut2(text,term_set)








# start = time()
# for x in xrange(10):
# 	for term in terms:
# 		if term not in dic:
# 			print term
# print len(terms),time() - start

# start = time()
# for x in xrange(10):
# 	for term in terms:
# 		if not search(trie,term):
# 			print term
# print len(terms),time() - start




terms = [x.strip().decode('utf8') for x in open('dic.txt') if len(x.strip())>0]
trie = build(terms)
segs =list(jieba.cut('nihao a'))
term_set = set(terms)
start = time()

for x in xrange(100):
	text  =open('../classification/data_train/culture/0').read().decode('utf8')
	cut(text, trie)

print time() - start

start = time()

for x in xrange(100):
	text  =open('../classification/data_train/culture/0').read().decode('utf8')
	segs =list(jieba.cut(text))

print time() - start

start = time()

for x in xrange(100):
	text  =open('../classification/data_train/culture/0').read().decode('utf8')
	segs =cut2(text,term_set)

print time() - start

