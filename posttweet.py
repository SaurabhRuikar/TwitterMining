# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:33:31 2019

@author: soura
"""

import tweepy

CONSUMER_KEY =""
CONSUMER_SECRET =""   
ACCESS_KEY = ""    
ACCESS_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
api.update_status('')