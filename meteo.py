import requests

def API_METEO():
       city = {'lyn':{},'prs':{},'lle':{},'mtp':{},'mrs':{},'tls':{},'nat':{},'bdr':{}}

       #LYON
       url = ('https://api.tomorrow.io/v4/timelines?location=45.764043,4.835659&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['lyn'] = response['data']['timelines'][0]['intervals'][0]

       #PARIS
       url = ('https://api.tomorrow.io/v4/timelines?location=48.866667,2.333333&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['prs'] = response['data']['timelines'][0]['intervals'][0]

       #MONTPELLIER
       url = ('https://api.tomorrow.io/v4/timelines?location=43.6112422,3.8767337&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['mtp'] = response['data']['timelines'][0]['intervals'][0]

       #LILLE
       url = ('https://api.tomorrow.io/v4/timelines?location=50.6365654,3.0635282&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['lle'] = response['data']['timelines'][0]['intervals'][0]

       #MARSEILLE
       url = ('https://api.tomorrow.io/v4/timelines?location=43.2961743,5.3699525&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['mrs'] = response['data']['timelines'][0]['intervals'][0]

       #NANTES
       url = ('https://api.tomorrow.io/v4/timelines?location=47.218371,-1.553621&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['nat'] = response['data']['timelines'][0]['intervals'][0]

       #TOULOUSE
       url = ('https://api.tomorrow.io/v4/timelines?location=43.604652,1.444209&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['tls'] = response['data']['timelines'][0]['intervals'][0]

       #BORDEAUX
       url = ('https://api.tomorrow.io/v4/timelines?location=44.837789,-0.57918&fields=temperature,cloudCover,precipitationType&timesteps=1d&units=metric&apikey=zarvog0e1SqxXZNuKzksMW4xcZkMtyUH')
       response = requests.get(url).json()
       city['bdr'] = response['data']['timelines'][0]['intervals'][0]

       for i in city:
              print(city[i])
              if city[i]['values']['precipitationType'] == 0:
                     if city[i]['values']['cloudCover'] > 60:
                            city[i]['values']['precipitationType'] = '☁️'
                     elif city[i]['values']['cloudCover'] >= 10 and city[i]['values']['cloudCover'] <= 60:
                            city[i]['values']['precipitationType'] = '⛅'
                     else :
                            city[i]['values']['precipitationType'] = '☀'
              elif city[i]['values']['precipitationType'] == 1:
                     city[i]['values']['precipitationType'] = '🌧'
              elif city[i]['values']['precipitationType'] == 2:
                     city[i]['values']['precipitationType'] = '🌨️'

       return ('#Prevision #meteo de la journée :'+
              '\n#Lyon '+str(int(city['lyn']['values']['temperature']))+'°C | '+city['lyn']['values']['precipitationType']+
              '\n#Marseille '+str(int(city['mrs']['values']['temperature']))+'°C | '+city['mrs']['values']['precipitationType']+
              '\n#Paris '+str(int(city['prs']['values']['temperature']))+'°C | '+city['prs']['values']['precipitationType']+
              '\n#Montpellier '+str(int(city['mtp']['values']['temperature']))+'°C | '+city['mtp']['values']['precipitationType']+
              '\n#Toulouse '+str(int(city['tls']['values']['temperature']))+'°C | '+city['tls']['values']['precipitationType']+
              '\n#Nantes '+str(int(city['nat']['values']['temperature']))+'°C | '+city['nat']['values']['precipitationType']+
              '\n#Bordeaux '+str(int(city['bdr']['values']['temperature']))+'°C | '+city['bdr']['values']['precipitationType']+
              '\n#Lille '+str(int(city['lle']['values']['temperature']))+'°C | '+city['lle']['values']['precipitationType'])
