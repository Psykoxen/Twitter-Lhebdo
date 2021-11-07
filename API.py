import json     #Module Json
import log              #Données Login
import time     #Module Time
import tweepy   #Module Twitter
import requests #Module requêtes
import xml              #Module XML

############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

############################################################### - INITIALISATION - ####################################################################

timeline = []
url = ('https://www.lexpress.fr/rss/alaune.xml')
certif = False

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

while certif == False:
        response = requests.get(url).text
        article = xml.xml_tools(response,'item')

        for i in article:
                already = False
                hst = open('hst.json')
                data = json.load(hst)
                hst.close()
                try:
                        latest = {'title':hashtag(replace(xml.xml_tools(i,'title')[0])),'img':xml.xml_image(str(i))}
                except:
                        latest = {'title':replace(xml.xml_tools(i,'title')[0]),'img':xml.xml_image(str(i))}
                for j in data['done']:
                        if latest['img'] == j['img']:
                                already = True
                for j in timeline:
                        if latest['img'] == j['img']:
                                already == True
                if not already:
                        timeline.append(latest)
                        print(time.ctime()+' | Add  ->'+timeline[-1]['title'])
                        break

        if not timeline:
                print('Nothing to tweet')
        else:
                try:
                        r = requests.get(timeline[0]['img'], allow_redirects=True)
                        open('tmp.png', 'wb').write(r.content)
                        api.update_with_media(filename='tmp.png',status='| #FRANCE | ~ '+timeline[0]['title'])
                        print(time.ctime()+' | Tweet -> '+timeline[0]['title'])
                        data['done'].append(timeline[0])
                        hst = open('hst.json',"w")
                        json.dump(data, hst, indent = 6)
                        hst.close()
                        timeline.pop(0)
                        time.sleep(2700)
                except:
                        api.update_status('| #FRANCE | ~ '+timeline[0]['title'])
                        data['done'].append(timeline[0])
                        hst = open('hst.json',"w")
                        json.dump(data, hst, indent = 6)
                        hst.close()
                        print(time.ctime()+' | Tweet -> '+timeline[0]['title'])
                        timeline.pop(0)
                        time.sleep(1800)