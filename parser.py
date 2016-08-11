import re

class Template(object):
    def __init__(self,text):
        if '|' not in text:
            self.name=text
            self.params={}
            return
        i=0
        nest=0
        params=[]
        currparam1=[] #This is the part of the current parameter after the equals sign if there is one. This should be the value of the parameter.
        currparam2=[] #This is the part of the current parameter before the equals sign if it exists. If the parameter is unnamed, there is no equals sign, and this is the empty list.
        curr=''
        name=''
        while i<len(text):
            if text[i]=='{' and i<len(text)-1 and text[i+1]=='{':
                if nest>0:
                    curr+='{{'
                else:
                    currparam1.append(curr)
                    curr=''
                nest+=1
                i+=2
                continue
            elif text[i]=='}' and i<len(text)-1 and text[i+1]=='}':
                nest-=1
                if nest>0:
                    curr+='}}'
                else:
                    currparam1.append(Template(curr))
                    curr=''
                i+=2
                continue
            elif text[i]=='|':
                if curr or not currparam1:
                    currparam1.append(curr)
                    curr=''
                if name=='':
                    name=currparam1
                else:
                    if currparam2:
                        params.append([currparam2,currparam1])
                    else:
                        params.append([None,currparam1])
                currparam1=[]
                currparam2=[]
                i+=1
                continue
            elif text[i]=='=':
                currparam1.append(curr)
                curr=''
                currparam2=currparam1
                currparam1=[]
                i+=1
                continue
            curr+=text[i]
            i+=1
        if curr or not currparam1:
            currparam1.append(curr)
            curr=''
        else:
            if currparam2:
                params.append([currparam2,currparam1])
            else:
                params.append([None,currparam1])
        self.params=params
        self.name=name

def parse(text):
    i=0
    nest=0
    parts=[]
    curr=''
    while i<len(text):
        if text[i]=='{' and i<len(text)-1 and text[i+1]=='{':
            if nest>0:
                curr+='{{'
                
            else:
                parts.append(curr)
                curr=''
            nest+=1
            i+=2
            continue
        if text[i]=='}' and i<len(text)-1 and text[i+1]=='}':
            nest-=1
            if nest>0:
                curr+='}}'
            else:
                parts.append(Template(curr))
                curr=''
            i+=2
            continue
        curr+=text[i]
        i+=1
    if nest>0:
        curr='{{'+curr
    if curr:
        parts.append(curr)
    return parts
