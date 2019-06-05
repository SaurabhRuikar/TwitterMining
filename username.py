#FOR SPECIFIC USERNAME
# -*- coding: utf-8 -*-
import tweepy 
import json


consumer_key= ""
consumer_secret= ""
access_key=""
access_secret=""

def get_tweets(username):
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    
    auth.set_access_token(access_key, access_secret) 
    
    api = tweepy.API(auth) 
    
    number_of_tweets=100
    tweets = api.user_timeline(screen_name=username) 
    
    File = open('username_results.json', 'w')
#Use csv Writer
#csvWriter = csv.writer(csvFile)
    list_dict=[]
    for tweet in tweets:
        dict_tweets={}
        dict_tweets["time"]=str(tweet.created_at)
        dict_tweets["tweet"]=tweet.text
        list_dict.append(dict_tweets)
    json.dump(list_dict,File,indent=4)
   
    
    #api = tweepy.API(auth)
    #tweets = api.home_timeline()
    #print(tweets)
#GET geo/id/:place_id


if __name__ == '__main__': 
    get_tweets("")  