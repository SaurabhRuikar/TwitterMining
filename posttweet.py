# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:33:31 2019

@author: soura
"""

import tweepy

CONSUMER_KEY ="e4YnfEaFGyWTjmOQZ1gKOpBT0"
CONSUMER_SECRET = "kCmDAkiLppvp7k5vu7bcuEhz7fM3GfqeBsGiYBSYBgMlhmxb1A"   
ACCESS_KEY = "1097772392372363264-B4BAsRTSagQzwR22fbvF3KMUzuhooM"    
ACCESS_SECRET = "mUwqVfD9UBajeAL9SMFaeV9s19jgjZtDVOyDYpG5qDFMj"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
api.update_status('Lets all meet and go craazy!')