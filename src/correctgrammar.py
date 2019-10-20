import sys
import re
import operator
from collections import OrderedDict
from collections import defaultdict
from random import shuffle
import random
import json
import codecs
import string

'''
def preprocessing():
    s=[]
    for line in open(str(sys.argv[1]), "r", errors='ignore'):
        line=line.rstrip('\n')
        l=line.split()
        c=0
        for words in l:
            if c==0:
                prevw='BOS/BOS'
            else:
                prevw=l[c-1]
            if c==len(l)-1:
                nextw='EOS/EOS'
            else:
                nextw=l[c+1]
#            prevword=prevw.split('/')
#            nextword=nextw.split('/')
#            currentword=words.split('/')
            
            currentwordtemp=words.split('/')
            currentword=words.split('/')[:-1]
            current='/'.join(currentword)

            if current=='it\'s' or current=='its' or current=='you\'re' or current=='your' or current=='they\'re' or current=='their' or current=='loose' or current=='lose' or current=='to' or current=='too':
                prevwordtemp=prevw.split('/')
                prevword=prevw.split('/')[:-1]
                prev='/'.join(prevword)
                
                nextwordtemp=nextw.split('/')
                nextword=nextw.split('/')[:-1]
                next='/'.join(nextword)

                s.append(current+' prev:'+prev+" prevtag:"+prevwordtemp[-1]+" next:"+next+" nexttag:"+nextwordtemp[-1])
#            s.append(currentwordtemp[-1]+' prev:'+prev+" current:"+current+" next:"+next+" prevtag:"+prevwordtemp[-2]+" currenttag:"+currentwordtemp[-2]+" nexttag:"+nextwordtemp[-2])

            c=c+1
    return [s]
'''

defclass=OrderedDict()


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

wordcount={}
#classes=OrderedDict()
totalmsg=0
sum=OrderedDict()
count=0
wavg=defaultdict(dict)

for line in open(str(sys.argv[1]), "r", errors='ignore'):
    wavg=json.loads(line)

i=0
#fo=open('output.txt', "a",  errors='ignore')

s=[]
sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
for sentence in sys.stdin:
    sent=sentence.split()
    c=0
    for words in sent:
        if c==0:
            prevw1='BOS/BOS'
            prevw2='BOS/BOS'
        else:
            if c==1:
                prevw2='BOS/BOS'
                prevw1=sent[c-1]
            else:
                prevw2=sent[c-2]
                prevw1=sent[c-1]

        if c==len(sent)-1:
            nextw1='EOS/EOS'
            nextw2='EOS/EOS'
        else:
            if c==len(sent)-2:
                nextw2='EOS/EOS'
                nextw1=sent[c+1]
            else:
                nextw1=sent[c+1]
                nextw2=sent[c+2]
#            prevword=prevw.split('/')
#            nextword=nextw.split('/')
#            currentword=words.split('/')
        
        currentwordtemp=words.split('/')
        currentword=words.split('/')[:-1]
        current='/'.join(currentword)

        if current.lower()=='it\'s' or current.lower()=='its' or current.lower()=='you\'re' or current.lower()=='your' or current.lower()=='they\'re' or current.lower()=='their' or current.lower()=='loose' or current.lower()=='lose' or current.lower()=='to' or current.lower()=='too':
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

            s.append(current.lower()+' prev2:'+prev2+" prev1:"+prev1+" prev1tag:"+prevword1temp[-1]+" next1:"+next1+" next2:"+next2)
#            print(s[0])
            for line in s:
                l=line.split()
                t=l[1:]
        #        print('*********')
        #        print(l[0])
                sum.clear()
#                print(l[0])
                for k,v in classes[l[0]].items():
        #            print(str(k))
                    sum[str(k)]=0
                    for word in t:
                        wavg[str(k)].setdefault(word, 0)
                        sum[str(k)]=sum[str(k)]+wavg[str(k)][word]
                
                value=list(sum.values())
                key=list(sum.keys())
                predclass=key[value.index(max(value))]
                            
        #        print(predclass+" "+defclass[l[0]])
                if(sum[defclass[l[0]]]>=sum[predclass]):
                    predclass=defclass[l[0]]
                    
                if (re.match('^[A-Z]+[a-z]+',current)):
                    predclass=string.capwords(predclass)

                sys.stdout.write(predclass+" ")
                del s[:]
        else:
            sys.stdout.write(current+" ")
        c=c+1
    sys.stdout.write('\n')
    sys.stdout.flush()
    