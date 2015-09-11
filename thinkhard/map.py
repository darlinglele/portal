import socket
f = open('ip.txt','w')
for x in open('domain.txt'):
  if len(x.strip())==0:
    continue
  ip =''
  try:
    ip = socket.gethostbyname(x.strip().split(':')[0].split('/')[0])
  except Exception,e:
    ip = str(e)
  f.write(ip+'\n')
f.close()
# print 'Done, please check the ip.txt file, bye bye....'
lst = set([x for x in open('ip.txt').readlines()])
print len(lst)
