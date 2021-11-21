import json     #Module Json
import log      #Données Login
import time     #Module Time
import tweepy   #Module Twitter
import requests #Module requêtes
import xml      #Module XML
import datetime #Module Datetime
############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

############################################################### - INITIALISATION - ####################################################################

timeline = []
url = ('https://www.lexpress.fr/rss/alaune.xml')
certif = False
meteo = 0

last = str(datetime.datetime.now().year)+'-'+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)
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

def covid_all(last):
        data = requests.get("https://coronavirusapifr.herokuapp.com/data/live/france").json()[0]
        if last != data['date']:
                message = '|#COVID19| ~ Journée du '+str(data['date'][-2:])+'/'+str(data['date'][-5:-3])+'/'+str(data['date'][:4])+' en #France\n-------------------------------\nNouveaux cas : '+str(data['conf_j1'])+'\nDécés : '+str(data['dchosp'])+' (+'+str(data['incid_dchosp'])+')\n-------------------------------\nOccupation : '+str(int(data['TO']*100))+'%\nHospitalisation : '+str(data['hosp'])+' (+'+str(data['incid_hosp'])+')\nRéanimation : '+str(data['rea'])+' (+'+str(data['incid_rea'])+')\n'
                api.update_status(message)
                print(time.ctime()+' | TWEET | Covid Data ')
                time.sleep(1800)
                return(data['date'])

while certif == False:
        try :
                if meteo != (api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['id']):
                        api.retweet(api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['id'])
                        print(time.ctime()+' | RETWEET | Meteo ')
                        meteo = api.user_timeline(user_id=1457877644184330248,count=20, tweet_mode = 'extended')[0]._json['id']
                        time.sleep(1800)
        except :
                print(time.ctime()+' | ERROR | No Meteo ')

        try :
                last = covid_all(last)
        except :
                print(time.ctime()+' | ERROR | No Covid Data ')                
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
                        print(time.ctime()+' | ADD | '+timeline[-1]['title'])
                        break

        if not timeline:
                print(time.ctime()+'| ERROR | Nothing to tweet')
        else:
                try:
                        r = requests.get(timeline[0]['img'], allow_redirects=True)
                        open('tmp.png', 'wb').write(r.content)
                        api.update_with_media(filename='tmp.png',status='| #FRANCE | ~ '+timeline[0]['title'])
                        print(time.ctime()+' | TWEET | '+timeline[0]['title'])
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
                        print(time.ctime()+' | TWEET | '+timeline[0]['title'])
                        timeline.pop(0)
                        time.sleep(1800)
