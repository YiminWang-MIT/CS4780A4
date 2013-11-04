import scipy.sparse as sp
from math import *


wordcount=0
with open("arxiv/arxiv.train") as f:
  for line in f:
    sep=line.partition(' ')
    line=sep[2]
    while line.find(':')>=0:
      sep=line.partition(':')
      wordid=int(sep[0])
      if wordid>wordcount: wordcount=wordid
      line=sep[-1]
      sep=line.partition(' ')
      line=sep[-1]
print "Word count"
word=[[0]*wordcount,[0]*wordcount]
cl=[0,0]
clword=[0,0]
with open("arxiv/arxiv.train") as f:
  for line in f:
    sep=line.partition(' ')
    line=sep[2]
    c=(int(sep[0]))
    c=(c+1)/2
    cl[c]+=1
    while line.find(':')>=0:
      sep=line.partition(':')
      wordid=int(sep[0])-1
      line=sep[-1]
      sep=line.partition(' ')
      occur=int(sep[0])
      clword[c]+=occur
      word[c][wordid]+=occur
      line=sep[-1]
print "Training"
for i in [0,1]:
  for wd in range(wordcount):
    word[i][wd]=log(1+word[i][wd])-log(wordcount+clword[i])
print "log"
conpro=sp.coo_matrix(word)
artwd=[]
artcl=[]
index=0
with open("arxiv/arxiv.test") as f:
  for line in f:
    artwd.append([0]*wordcount)
    sep=line.partition(' ')
    line=sep[2]
    c=(int(sep[0]))
    c=(c+1)/2
    artcl.append(c)
    while line.find(':')>=0:
      sep=line.partition(':')
      wordid=int(sep[0])-1
      line=sep[-1]
      sep=line.partition(' ')
      occur=int(sep[0])
      artwd[index][wordid]=occur
      line=sep[-1]
    index+=1
    print index
print "input done"

testdoc=sp.coo_matrix(artwd)
predict=testdoc*(conpro.transpose())

#partA
tp=0
fpos=0
fneg=0
for i in range(index):
  neg=predict[i][0]+log(cl[0]/(cl[0]+cl[1]))
  pos=predict[i][1]+log(cl[1]/(cl[0]+cl[1]))
  cls=0
  if pos>neg: cls=1
  if cls==artcl[i]: 
    tp+=1
  elif cls==1:
    fpos+=1
  else: fneg+=1
print "---PartA---"
print "F pos = %d"%fpos
print "F neg = %d"%fneg
print "Correct = %d"%tp
print "Total = %d"%index
acc=float(tp)/index
print "Accuracy = %f"%acc

#partB
tp=0
fpos=0
fneg=0
for i in range(index):
  neg=1+predict[i][0]+log(cl[0]/(cl[0]+cl[1]))
  pos=10+predict[i][1]+log(cl[1]/(cl[0]+cl[1]))
  cls=0
  if pos>neg: cls=1
  if cls==artcl[i]: 
    tp+=1
  elif cls==1:
    fpos+=1
  else: fneg+=1

print "---PartB---"
print "F pos = %d"%fpos
print "F neg = %d"%fneg
print "Correct = %d"%tp
print "Total = %d"%index
acc=float(tp)/index
print "Accuracy = %f"%acc
