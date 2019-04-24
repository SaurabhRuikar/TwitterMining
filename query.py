
import re 
import tweepy 
from tweepy import OAuthHandler 
#from textblob import TextBlob
import json 
  
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'e4YnfEaFGyWTjmOQZ1gKOpBT0'
        consumer_secret = 'kCmDAkiLppvp7k5vu7bcuEhz7fM3GfqeBsGiYBSYBgMlhmxb1A'
        access_token = '1097772392372363264-B4BAsRTSagQzwR22fbvF3KMUzuhooM'
        access_token_secret = 'mUwqVfD9UBajeAL9SMFaeV9s19jgjZtDVOyDYpG5qDFMj'
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def fetch_multi_query(self,query_list):
    	for query in query_list:
    		print(self.get_tweets(query,count=50))
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
            File = open('query_results.json', 'w')
            list_dict=[]
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
              dict_tweets={}
              dict_tweets["time"]=str(tweet.created_at)
              dict_tweets["tweet"]=tweet.text
              list_dict.append(dict_tweets)
            json.dump(list_dict,File,indent=4)
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 

  
def fetch_queries(query_list): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    #tweets = api.get_tweets(query = 'India Terrorist', count =10) 
    #print(tweets)
    api.fetch_multi_query(query_list)
  
if __name__ == "__main__": 
    # calling main function 
    main() 

