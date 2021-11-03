import json 	#Module Json
import log 		#Données Login
import time 	#Module Time
import tweepy 	#Module Twitter
import requests #Module requêtes
import xml 		#Module XML

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

while certif == False:
	response = requests.get(url).text
	article = xml.xml_tools(response,'item')

	for i in article:
		already = False
		hst = open('hst.json')
		data = json.load(hst)
		hst.close()
		latest = {'title':hashtag(xml.xml_tools(i,'title')[0]),'img':xml.xml_image(str(i))}
		for j in data['done']:
			if latest['img'] == j['img']:
				already = True
		for j in timeline:
			if latest['img'] == j['img']:
				already == True
		if not already:
			timeline.append(latest)
			print(' Add  ->'+timeline[-1]['title'])
			break

	if not timeline:
		print('Nothing to tweet')
	else:		
		try:
			r = requests.get(data['done'][last]['img'], allow_redirects=True)
			open('tmp.png', 'wb').write(r.content)
			api.update_with_media(filename='tmp.png',status='| #FRANCE | ~ '+timeline[0]['title'])
			print('Tweet -> '+timeline[0]['title'])
			data['done'].append(timeline[0])
			hst = open('hst.json',"w")
			json.dump(data, hst, indent = 6)
			hst.close()
			timeline.pop(0)
			time.sleep(3600)
		except:
			api.update_status('| #FRANCE | ~ '+timeline[0]['title'])
			data['done'].append(timeline[0])
			hst = open('hst.json',"w")
			json.dump(data, hst, indent = 6)
			hst.close()
			print('Tweet -> '+timeline[0]['title'])
			timeline.pop(0)
			time.sleep(3600)
