import sys
import os
#import APP.twitter_credentials              #añadir/eliminar app
#from APP.utility_functions import *         #modulo eliminar/ servidor añadir
import codecs
import preprocessor as p
import tweepy
import csv
import json
import copy
import tweepy as tw
from twython import Twython
import pandas as pd
import numpy as np


# credenciales de la cuenta de twitter
from app_package.utility_functions import *
import app_package.twitter_credentials as tc

#from utility_functions import *
#import twitter_credentials as tc


# credenciales de la cuenta de twitter
consumer_key = tc.CONSUMER_KEY
consumer_secret = tc.CONSUMER_SECRET
access_key = tc.ACCESS_TOKEN
access_secret = tc.ACCESS_TOKEN_SECRET



def get_profileTwython(username):

    twitter = Twython(tc.CONSUMER_KEY, tc.CONSUMER_SECRET, tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
    twitter.verify_credentials()
    #twitter.get_home_timeline()

    profile= twitter.show_user(screen_name= '_alexgalo')

    name = profile['name']
    profile_img = profile['profile_image_url']
    username = profile['screen_name']
    location = profile['location']
    created_at = profile['created_at']
    post = profile['statuses_count']
    followers = profile['followers_count']
    following = profile['friends_count']
    description = profile['description']

    # Almacena la información relacionada al perfil.
    user_profile_Y = dict()

    user_profile_Y = {'name': name,
                    'username': username,
                    'location': location,
                    'created_at': created_at,
                    'post': post,
                    'followers': followers,
                    'following': following,
                    'description': description,
                    'profile_img': profile_img

    }

    print('~ PERFIL OBTENIDO VÍA TWEEPY')
    statusFlag= True

    return user_profile_Y

def get_profile(username): 

    if(consumer_key == ''):
        print('Es necesario contar con accesos a la API de Twitter.')
        return 
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    
    profile = api.get_user(screen_name=username)

    profile_img = profile.profile_image_url
    name = profile.name
    username = profile.screen_name
    location = profile.location
    created_at = profile.created_at
    post = profile.statuses_count
    followers = profile.followers_count
    following = profile.friends_count
    description = profile.description


    # Almacena la información relacionada al perfil.
    user_profile = dict()

    user_profile = {'name': name,
                    'username': username,
                    'location': location,
                    'created_at': created_at,
                    'post': post,
                    'followers': followers,
                    'following': following,
                    'description': description,
                    'profile_img': profile_img

    }

    # access to a element
    #print(user_profile['name'])

    print('~OBTENIENDO PERFIL ...')
    statusFlag= True

    return user_profile



def twitterStatistics(username):

    if(consumer_key == ''):
        print('Es necesario contar con accesos a la API de Twitter.')
        return 

    # Acceso al API de Twitter.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    tweets = api.user_timeline(screen_name=username, count=100)
    

    # Creamos una dataframe de pandas:
    data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])


    # Añadimos los datos relevantes:
    data['longitud']  = np.array([len(tweet.text) for tweet in tweets])
    data['ID']   = np.array([tweet.id for tweet in tweets])
    data['Fecha'] = np.array([tweet.created_at for tweet in tweets])
    data['Fuente'] = np.array([tweet.source for tweet in tweets])
    data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
    data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])


    # Sacamos la media de las longitudes:
    mean = np.mean(data['longitud'])
    

    # Sacamos el tweet con más "Me gusta" y el más retuiteado:
    fav_max = np.max(data['Likes'])
    rt_max = np.max(data['RTs'])

    fav = data[data.Likes == fav_max].index[0]
    rt  = data[data.RTs == rt_max].index[0]


    # Obtener todas las fuentes posibles:
    fuentes = []
    for fuente in data['Fuente']:
        if fuente not in fuentes:
            fuentes.append(fuente)


    # Almacena la información relacionada al contenido del perfil.
    tweet_stats = dict()

    tweet_stats = {
        'long_media': int(mean),

        'tweet_fav': data['Tweets'][fav],
        'tweet_num_favs': fav_max,
        'tweet_fav_chr': data['longitud'][fav],

        'tweet_rt': data['Tweets'][rt],
        'tweet_num_rt': rt_max, 
        'tweet_rt_chr': data['longitud'][rt],
        'creacion_contenido': fuentes
    }

    print('~CALCULANDO ESTADISTICAS DE TWITTER...')

    return tweet_stats




def get_UserTimeline(screen_name):
    


    if (consumer_key == ''):
        print('Es necesario contar con accesos a la API de Twitter')
        return


    # Acceso al API de Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)


    # inicializa un lista para almacenar los tuits
    alltweets = []


    print('~OBTENIENDO EL TIMELINE...')

    # hace una primera consulta de 200 tuits
    try:
        new_tweets = api.user_timeline(screen_name = screen_name, count = 200)
    except tweepy.TweepError:
        print ('Error! No se encontró el usuario')

    # guarda los mas recientes tuits
    alltweets.extend(new_tweets)

    # guarda el ID del penultimo item
    oldest = alltweets[-1].id - 1

    # mientras existan tweets por guardar
    while len(new_tweets) > 0:

        # se utiliza el parametro max_id para evitar duplicados
        new_tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id = oldest)

        # añade la nueva lista de tweets
        alltweets.extend(new_tweets)

        # actualiza el id del tweet mas viejo
        oldest = alltweets[-1].id - 1

        print('... %s tuits descargados hasta ahora' % (len(alltweets)))
  


    # transforma los tweets de tweepy en una lista [[id, created_at, text]]
    data = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    # almacena todos los tweet del timeline
    totalText = ''  

    los_indeseables = ['!', '"', '#', '%', '&', '/', '(', ')', '=', '?', '¿', '¡', '*', '+', '~', '[', '{', '^', '}', ']', ';', ',', ':', '.', '_', '-', '\\', '<', '>', '', '►', '»', '«', '—']

    totalText = list()

    text = ''


    counter_text = 0
    
    # PREPROCESAMIENTO DEL TIMELINE
    for tweet in range(len(data)):
            
        text = data[tweet][2]
                
        if('RT @' not in text):
                    
            text = p.tokenize(text)
            text = text.lower()
            text = remove_accents(text)
            text = replace_symbols(text, los_indeseables, '')

            totalText.append(text)
            counter_text = counter_text + 1

    
    
    print('~LONGITUD DEL TIMELINE no RT:', len(totalText) )

    


    return totalText, alltweets



def twitterActivity(username, alltweets):

    print('ACTIVIDAD RECIENTE')

    import datetime
    import copy

    # Fecha actual
    date = datetime.datetime.now()
    actualYear = date.year
    actualMonth = date.month



    # diccionario MES
    month = {}
    month = {
        "Name": '',
        "Month": 0,
        "Tweets": 0,
    }


    # Se obtienen los meses
    month1 = copy.deepcopy(month)
    month1["Month"] = actualMonth

    month2 = copy.deepcopy(month)
    month2["Month"] = actualMonth - 1

    month3 = copy.deepcopy(month)
    month3["Month"] = actualMonth - 2


    # Cuenta los tuits de los últimos tres meses
    for tweet in range(len(alltweets)):
        
        # Fecha del tuit
        Tweet = alltweets[tweet]
        tweetDate = Tweet.created_at
        tweetYear = tweetDate.year
        tweetMonth = tweetDate.month

        if(actualYear == tweetYear):

            if(tweetMonth == month1["Month"]):
                month1["Tweets"] = month1["Tweets"] + 1

            if(tweetMonth == month2["Month"]):
                month2["Tweets"] = month2["Tweets"] + 1

            if(tweetMonth == month3["Month"]):
                month3["Tweets"] = month3["Tweets"] + 1


    print('$$$')
    #print(month1)
    
    # Lista de diccionarios
    Activity = list()
    Activity.append(month1)
    Activity.append(month2)
    Activity.append(month3)
    
    
    for dic in range(len(Activity)):

        if(Activity[dic]["Month"] == 1):
            Activity[dic]["Name"] = 'Enero'

        if(Activity[dic]["Month"] == 2):
            Activity[dic]["Name"] = 'Febrero'

        if(Activity[dic]["Month"] == 3):
            Activity[dic]["Name"] = 'Marzo'

        if(Activity[dic]["Month"] == 4):
            Activity[dic]["Name"] = 'Abril'

        if(Activity[dic]["Month"] == 5):
            Activity[dic]["Name"] = 'Mayo'
                
        if(Activity[dic]["Month"] == 6):
            Activity[dic]["Name"] = 'Junio'
                
        if(Activity[dic]["Month"] == 7):
            Activity[dic]["Name"] = 'Julio'
        
        if(Activity[dic]["Month"] == 8):
            Activity[dic]["Name"] = 'Agosto'
        
        if(Activity[dic]["Month"] == 9):
            Activity[dic]["Name"] = 'Septiembre'
        
        if(Activity[dic]["Month"] == 10):
            Activity[dic]["Name"] = 'Octubre'
        
        if(Activity[dic]["Month"] == 11):
            Activity[dic]["Name"] = 'Noviembre'
        
        if(Activity[dic]["Month"] == 12):
            Activity[dic]["Name"] = 'Diciembre'
    

    print(Activity[0])
    print(Activity[1])
    print(Activity[2])


    ActivityN = ['', '', '']
    ActivityN.insert(2, Activity[0]["Name"])
    ActivityN.insert(1, Activity[1]["Name"])
    ActivityN.insert(0, Activity[2]["Name"])

    ActivityV = [0, 0, 0]
    ActivityV.insert(2, Activity[0]["Tweets"])
    ActivityV.insert(1, Activity[1]["Tweets"])
    ActivityV.insert(0, Activity[2]["Tweets"])

    print('~CALCULANDO ACTIVIDAD RECIENTE...')
    
    

    return ActivityN, ActivityV






"""
if __name__ == '__main__':
    if(len(sys.argv) == 2):

        get_UserTimeline(sys.argv[1])
    
    else:
        print('ERROR !')
"""