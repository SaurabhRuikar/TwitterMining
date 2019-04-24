# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:26:01 2019

@author: soura
"""
import hashtag
import query 
import username
import json
import decider
import pandas as pd

class Transfer:
    def __init__(self):
        self.file_mapping = {"query":"query_results.json", "username":"username_results.json","hashtag":"hashtag_results.json"}
        self.predictor=decider.Decider(mode="test")
    def set_mode(self, mode):
        self.mode = mode
    def fetch_predict(self, data):
        filename = self.file_mapping[self.mode]
        if self.mode=="query":
            query.fetch_queries(data)
        elif self.mode=="username":
            username.get_tweets(data)
        else:
            hashtag.get_tweets(data)
        data=json.load(open(filename,'r'))
        tweets=[]
        for obj in data:
            tweets.append(obj['tweet'])
        predictions=[self.predictor.predict(tweets[i])[0] for i in range(len(tweets))]
        return pd.DataFrame({"Tweets":tweets,"Prediction":predictions})