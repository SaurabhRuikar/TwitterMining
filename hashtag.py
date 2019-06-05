#for specific hastag on twitter
import tweepy
import pandas as pd
import json
####input your credentials here
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Open/Create a file to append data
#Use csv Writer
#csvWriter = csv.writer(csvFile)
def get_tweets(query):
    list_dict=[]
    for tweet in tweepy.Cursor(api.search,q=query,
                           lang="en",
                           since="2017-04-03").items(100):
        dict_tweets={}
        dict_tweets["time"]=str(tweet.created_at)
        dict_tweets["tweet"]=str(tweet.text)
        list_dict.append(dict_tweets)
    File = open('hashtag_results.json', 'w')
    json.dump(list_dict,File,indent=4)
    File.close()
