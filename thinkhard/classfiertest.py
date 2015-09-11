from classifier import Classifier
import math
import sys
print sys.path

# C= (c1, c2)
# p1=p(c1) =1/2
# p2=p(c2)=1/2

# H(C) = -(p1*log(p1)+p2*log(p2))
p1= 0.5
p2 = 0.5
p_lst= [p1,p2]
h = -sum([x*math.log(x,2) for x in p_lst])
print h

print math.log(2.0/3,2)

# H(C|T) = p(T1)*H(C|T1)+p(T2)*H(C|T2)
# p1 = p(C1|T1)
# p2 = p(C2|t2)
# H(C|T1)= -(p1*log(p1))
# Information gain
# IG = H(C) - H(C|T)
# H(C) -

d1 = {'content': 'c d', 'category':'c1'}
d2 = {'content': 'b d', 'category':'c1'}
d3 = {'content': 'a d', 'category':'c2'}
d4 = {'content': 'a c', 'category':'c2'}

terms ={
  'a':{'category_count':{'c1':2,'c2':0},'document_count':2},
  'b':{'category_count':{'c1':1,'c2':0},'document_count':1},
  'c':{'category_count':{'c1':1,'c2':1},'document_count':2},
  'd':{'category_count':{'c1':1,'c2':2},'document_count':3}}

categories ={'c1':2,'c2':2}

classifier = Classifier()
classifier.select(data={'terms':terms,'categories':categories})
print classifier.selected_terms
