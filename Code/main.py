import json     #Module Json
import log      #Données Login
import time     #Module Time
import tweepy   #Module Twitter
import requests #Module requêtes
import xml      #Module XML
import datetime #Module Datetime
from rich import print
############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

############################################################### - INITIALISATION - ####################################################################

timeline = []
url = ('https://www.lexpress.fr/rss/alaune.xml')
check = True
meteo = 0
covid = 0


hst = open('hst.json')
data = json.load(hst)
hst.close()

################################################################## - MAIN - ####################################################################

def hashtag(text):
        result = requests.get("http://127.0.0.1:5000/hashtag/" +text)
        return json.loads(result.text)['hashtaged']

def replace(text):
        text = text.replace("&amp;","&")
        text = text.replace("&quot;",'"')
        text = text.replace("&apos;","'")
        text = text.replace("&gt;",">")
        text = text.replace("&lt;","<")
        text = text.replace("&#039;","'")
        return text

while True:
        try :
                if meteo != (api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['id']) and '|#COVID19|' in api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['full_text']:
                        for i in ["🔴","🟠","🟡","🟢"]:
                                if i in api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['full_text']:
                                        check = False
                        if check == True:
                                api.retweet(api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['id'])
                                print('[bold light_goldenrod1]'+time.ctime()+' | RETWEET | Meteo [/bold light_goldenrod1]')
                                meteo = api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['id']
                                time.sleep(1800)
                        else:
                                check = True
        except :
                print('[bold bright_red]'+time.ctime()+' | ERROR | Meteo [/bold bright_red]')

        try :
                if covid != (api.user_timeline(user_id=1476300686165954564,count=20,tweet_mode='extended')[0]._json['id']):
                        api.retweet(api.user_timeline(user_id=1476300686165954564,count=20,tweet_mode='extended')[0]._json['id'])
                        print('[bold light_goldenrod1]'+time.ctime()+' | RETWEET | Covid [/bold light_goldenrod1]')
                        covid = api.user_timeline(user_id=1476300686165954564,count=20,tweet_mode='extended')[0]._json['id']
                        time.sleep(1800)
        except :
                print('[bold bright_red]'+time.ctime()+' | ERROR | Covid Data [/bold bright_red]')                
        
        
        response = requests.get(url).text
        article = xml.xml_tools(response,'item')

        for i in article:
                already = False
                hst = open('hst.json')
                data = json.load(hst)
                hst.close()
                try :
                        if len(hashtag(replace(xml.xml_select(xml.xml_tools(i,'description')[0],'<![CDATA[')[0]))) <= 266:
                                latest = {'title':hashtag(replace(xml.xml_select(xml.xml_tools(i,'description')[0],'<![CDATA[')[0])),'img':xml.xml_image(str(i))}
                        else:
                                latest = {'title':hashtag(replace(xml.xml_tools(i,'title')[0]))+'.','img':xml.xml_image(str(i))}   
                except:
                        if len(replace(xml.xml_select(xml.xml_tools(i,'description')[0],'<![CDATA[')[0])) <= 266:
                                latest = {'title':replace(xml.xml_select(xml.xml_tools(i,'description')[0],'<![CDATA[')[0]),'img':xml.xml_image(str(i))}
                        else:
                                latest = {'title':replace(xml.xml_tools(i,'title')[0])+'.','img':xml.xml_image(str(i))}
                        
                for j in data['done']:
                        if latest['img'] == j['img']:
                                already = True
                for j in timeline:
                        if latest['img'] == j['img']:
                                already == True
                if not already:
                        timeline.append(latest)
                        print('[bold light_slate_blue]'+time.ctime()+' | ADD | '+timeline[-1]['title']+'[/bold light_slate_blue]')
                        break

        if not timeline:
                print('[bold sandy_brown]'+time.ctime()+'| ERROR | Nothing to tweet [/bold sandy_brown]')
        else:
                try:
                        r = requests.get(timeline[0]['img'], allow_redirects=True)
                        open('tmp.png', 'wb').write(r.content)
                        api.update_with_media(filename='tmp.png',status='| #FRANCE | ~ '+timeline[0]['title'])
                        print('[bold green4]'+time.ctime()+' | TWEET | '+timeline[0]['title']+'[/bold green4]')
                        data['done'].append(timeline[0])
                        hst = open('hst.json',"w")
                        json.dump(data, hst, indent = 6)
                        hst.close()
                        timeline.pop(0)
                        time.sleep(2400)
                except:
                        api.update_status('| #FRANCE | ~ '+timeline[0]['title'])
                        data['done'].append(timeline[0])
                        hst = open('hst.json',"w")
                        json.dump(data, hst, indent = 6)
                        hst.close()
                        print('[bold green4]'+time.ctime()+' | TWEET | '+timeline[0]['title']+'[/bold green4]')
                        timeline.pop(0)
                        time.sleep(1800)