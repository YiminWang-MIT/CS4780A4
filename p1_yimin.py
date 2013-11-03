import sys
import os
from math import *
import random

def svm(name, clist, d):
  optclist=[0]*10
  classlist=[]
  for digit in range(10):
    path=name+"/"
    trainfile=name+"%d.train"%digit
    valfile=name+"%d.val"%digit
    bestacc=0
    for c in clist:
      classfile="classifier/"+name+"_%d_%d_%f.class"%(digit,d,c)
      if d==1:
        os.system("./svm_learn -c %f %s %s > log"%(c,path+trainfile,path+classfile))
      else:
        os.system("./svm_learn -c %f -t 1 -d %d %s %s > log"%(c,d,path+trainfile,path+classfile))
      acc=cal_acc(path+valfile,[path+classfile],[1])
      if acc>bestacc: 
        optclist[digit]=c
        bestacc=acc
    classlist.append(path+"classifier/"+name+"_%d_%d_%f.class"%(digit,d,optclist[digit]))
  print optclist
  testfile=name+".test"
  return cal_acc(path+testfile,classlist,[10]+range(1,10))

def cal_acc(test,clas,typ):
  index=0
  truth=[]
  f=file(test,"r")
  for line in f: truth.append(int(line.partition(' ')[0]))
  predict=[]*len(typ)
  for ty, cl in zip(typ,clas):
    outfile="digits/output/%d.result"%ty
    os.system("./svm_classify %s %s %s > log"%(test,cl,outfile))
    predict.append([])
    f=file(outfile,"r")
    for line in f: predict[index].append(float(line))
    index+=1
  cor=0
  for i,t in enumerate(truth):
    bestp=-9999
    bestindex=-1
    for index in range(len(typ)):
      if predict[index][i]>bestp:
        bestp=predict[index][i]
        bestindex=index
    if len(typ)<=1:
      if predict[0][i]*t>0: cor+=1
    else:
      if (typ[bestindex]==t): cor+=1
  return float(cor)/len(truth)

clist=[0.00001,0.00005,0.0001,0.0005,0.001,0.005,0.01,0.05,0.1]
dlist=[1,2,3,4,5]
for d in dlist:
  print "d=%d, Accuracy=%f"%(d,svm("digits",clist,d))
