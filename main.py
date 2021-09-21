# -*- coding: utf-8 -*-
import requests
import tweepy
import log
import json
import uuid
import xml
from datetime import datetime
import meteo

############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

############################################################### - IINIALISATION - ####################################################################

timeline = []
url = ('https://www.francetvinfo.fr/titres.rss')
weather = False

################################################################## - PRINCIPAL - ####################################################################

while True:
	response = requests.get(url).text
	article = xml.xml_tools(response,'item')
	if datetime.now().hour >= 8 and datetime.now().hour <= 9 and datetime.now().minute <= 30 and weather == False:
		api.update_status(meteo.API_METEO())
		weather = True
	if datetime.now().hour > 9 and weather == True:
		weather = False

	for i in article:
		hst = open('hst.json')
		data = json.load(hst)
		hst.close()
			
		new = True
		for uid in data['done']:
			if uid == uuid.uuid3(uuid.NAMESPACE_DNS,xml.xml_image(str(i))).hex :
				new = False
		if new == True:

			timeline.append({'title':xml.semantique(xml.xml_tools(i,'title')[0]),'img':xml.xml_image(str(i))})
			data['done'].append(str(uuid.uuid3(uuid.NAMESPACE_DNS,timeline[-1]['img']).hex))
				
			hst = open("hst.json", "r+")
			json.dump(data, hst, indent = 6)
			hst.close()

	if timeline != []:
		try :                         
			r = requests.get(timeline[0]['img'], allow_redirects=True)
			open('tmp.png', 'wb').write(r.content)
			api.update_with_media(filename='tmp.png',status=timeline[0]['title']+' (francetvinfo.fr)\n|| #INFO'+timeline[0]['tag']+' ||')
		except:
			api.update_status(timeline[0]['title']+' (francetvinfo.fr)\n|| #INFO #NEWS #ACTU ||')
		print('Tweet !')
		timeline.pop(0)
		time.sleep(6000)
