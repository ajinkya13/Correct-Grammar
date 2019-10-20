import sys
import re
import operator
from collections import OrderedDict
from collections import defaultdict
from random import shuffle
import random
import json

def preprocessing():
    s=[]
    for line in open(str(sys.argv[1]), "r", errors='ignore'):
        line=line.rstrip('\n')
        l=line.split()
        c=0
        for words in l:
            if c==0:
                prevw1='BOS/BOS'
                prevw2='BOS/BOS'
            else:
                if c==1:
                    prevw2='BOS/BOS'
                    prevw1=l[c-1]
                else:
                    prevw2=l[c-2]
                    prevw1=l[c-1]

            if c==len(l)-1:
                nextw1='EOS/EOS'
                nextw2='EOS/EOS'
            else:
                if c==len(l)-2:
                    nextw2='EOS/EOS'
                    nextw1=l[c+1]
                else:
                    nextw1=l[c+1]
                    nextw2=l[c+2]
#            prevword=prevw.split('/')
#            nextword=nextw.split('/')
#            currentword=words.split('/')
            
            currentwordtemp=words.split('/')
            currentword=words.split('/')[:-1]
            current='/'.join(currentword)

            if current=='it\'s' or current=='its' or current=='you\'re' or current=='your' or current=='they\'re' or current=='their' or current=='loose' or current=='lose' or current=='to' or current=='too':
                prevword1temp=prevw1.split('/')
                prevword1=prevw1.split('/')[:-1]
                prev1='/'.join(prevword1)
                
                prevword2temp=prevw2.split('/')
                prevword2=prevw2.split('/')[:-1]
                prev2='/'.join(prevword2)

                nextword1temp=nextw1.split('/')
                nextword1=nextw1.split('/')[:-1]
                next1='/'.join(nextword1)

                nextword2temp=nextw2.split('/')
                nextword2=nextw2.split('/')[:-1]
                next2='/'.join(nextword2)

                s.append(current+' prev2:'+prev2+" prev1:"+prev1+" prev1tag:"+prevword1temp[-1]+" next1:"+next1+" next2:"+next2)
#            s.append(currentwordtemp[-1]+' prev:'+prev+" current:"+current+" next:"+next+" prevtag:"+prevwordtemp[-2]+" currenttag:"+currentwordtemp[-2]+" nexttag:"+nextwordtemp[-2])

            c=c+1
    return [s]


wordcount={}
classes=OrderedDict()
totalmsg=0
sum=OrderedDict()
defclass=OrderedDict()

s=[]
s=preprocessing()
#fo=open('trainingfile.txt', "a")
#print(s[0])
#fo.close()
'''
print(s[0][0])
print(s[0][1])
print(s[0][2])
'''
'''
for line in s[0]:
    line=line.rstrip('\n')
    l=line.split()
    t=l[1:]
    classes[l[0]]='true'
'''

classes=defaultdict(dict)

classes['its']['its']='true'
classes['its']['it\'s']='true'

classes['it\'s']['its']='true'
classes['it\'s']['it\'s']='true'

defclass['its']='its'
defclass['it\'s']='its'

classes['your']['you\'re']='true'
classes['your']['your']='true'

classes['you\'re']['you\'re']='true'
classes['you\'re']['your']='true'

defclass['your']='your'
defclass['you\'re']='your'

classes['their']['their']='true'
classes['their']['they\'re']='true'

classes['they\'re']['they\'re']='true'
classes['they\'re']['their']='true'

defclass['their']='their'
defclass['they\'re']='their'

classes['loose']['loose']='true'
classes['loose']['lose']='true'

classes['lose']['loose']='true'
classes['lose']['lose']='true'

defclass['loose']='lose'
defclass['lose']='lose'

classes['too']['to']='true'
classes['too']['too']='true'

classes['to']['too']='true'
classes['to']['to']='true'

defclass['too']='to'
defclass['to']='to'

#defclass = list(classes.keys())

w=defaultdict(dict)
wavg=defaultdict(dict)
c=1

for line in s[0]:
    line=line.rstrip('\n')
    l=line.split()
    t=l[1:]
    for k,v in classes[l[0]].items():
        for word in t:
            w[str(k)][word]=0
            wavg[str(k)][word]=0

#print(wavg['to']['prev:years'])       
            
#print(wavg['too']['prev:years'])       
i=0

ecount=0
count=0
error=0
preverror=0


for i in range(50): 
    count=0
    ecount=0
    random.shuffle(s[0])
    print("Iteration"+str(i)+"\n")
    for line in s[0]:
        count=count+1
        line=line.rstrip('\n')
        l=line.split()
        t=l[1:]
#        print('*********')
#        print(l[0])
        sum.clear()
        for k,v in classes[l[0]].items():
#            print(str(k))
            sum[str(k)]=0
            for word in t:
                sum[str(k)]=sum[str(k)]+w[str(k)][word]
        
        value=list(sum.values())
        key=list(sum.keys())
        predclass=key[value.index(max(value))]
                    
#        print(predclass+" "+defclass[l[0]])
        if(sum[defclass[l[0]]]>=sum[predclass]):
            predclass=defclass[l[0]]
        if l[0]!=predclass:
            ecount=ecount+1
            for word1 in t: #set(t):
                wavg[l[0]][word1]=wavg[l[0]][word1]+c
                wavg[predclass][word1]=wavg[predclass][word1]-c
                w[l[0]][word1]=w[l[0]][word1]+1
                w[predclass][word1]=w[predclass][word1]-1
        
        c=c+1
    print(str(ecount)+" "+str(count))
    error=float(ecount)/float(count)
    delta=preverror-error
    preverror=error
    print("Error: "+str(error))        
    print("Delta Error: "+str(delta))        
        
fo=open(str(sys.argv[2]), "a",  errors='ignore')

for k,v in classes.items():
    for l,m in wavg[str(k)].items():
        wavg[str(k)][str(l)]=float(w[str(k)][str(l)])-(float(wavg[str(k)][str(l)])/c)
fo.write(json.dumps(wavg))


fo.close()
