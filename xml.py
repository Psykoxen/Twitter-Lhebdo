# -*- coding: utf-8 -*-
import json
import requests

def xml_tools(myhtml,tag):
       res= []
       _tag = "</"+tag+">"
       end_tag = "<"+tag+">"
       for item in myhtml.split(_tag):
              if end_tag in item:
                     res.append(item [ item.find(end_tag)+len(end_tag) : ])
       return res

def xml_image(xhtml):
       find= 'url="'
       j = str(xhtml).index(find)
       end = str(xhtml)[j+len(find):].index('"')
       url = xhtml[j+len(find):j+len(find)+end]
       return(url)

def semantique(txt):
       result = requests.get("http://127.0.0.1:5000/hashtag/" +txt) 
       rep = json.loads(result.text)['hashtaged']
       return rep