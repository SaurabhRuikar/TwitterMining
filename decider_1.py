import pandas as pd
import spacy
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
import pickle
import sentiment
import numpy as np


nlp=spacy.load('en_core_web_sm')
class Decider:
    def __init__(self,mode="test"):
        if mode == 'train':
            self.model= RandomForestClassifier(n_estimators=250,criterion='entropy',verbose=10,random_state=3,n_jobs=-1,oob_score=True,)
            self.sentiment_model=RandomForestClassifier(n_estimators=50,criterion='entropy',n_jobs=-1,verbose=10)
            #self.model = MultinomialNB()
            self.vectorizer = TfidfVectorizer(min_df=3)
        else:
            self.model= load('rf.joblib')
            self.sentiment_model=load('sentiment_model.joblib')
            self.model.verbose=0
            self.vectorizer= pickle.load(open('vectorizer.b','rb'))
    def find_sentiments(self,tweets):
        positive_sentiment_score=[]
        negative_sentiment_score=[]
        for tweet in tweets:
            score=sentiment.calculate_sentiment(tweet)
            positive_sentiment_score.append(score['pos'])
            negative_sentiment_score.append(score['neg'])
        return positive_sentiment_score,negative_sentiment_score
    def load_data(self):
        dataframe=pd.read_csv('result.tsv',sep='\t')
        return dataframe.iloc[:,-1],dataframe.iloc[:,2]

    def preprocess(self,lines):
        for i in range(len(lines)):
            doc=nlp(lines[i])
            doc=[tok for tok in doc if str(tok) not in string.punctuation]
            doc=[tok for tok in doc if not tok.is_digit]
            doc=[tok.lemma_.lower().strip() for tok in doc if not tok.is_stop and tok.lemma_!='-PRON-']
            lines[i]=' '.join(doc)

    def train(self):
        labels,tweets=self.load_data()
        pos_sent,neg_sent=self.find_sentiments(tweets)
        self.preprocess(tweets)
        buffer_df=pd.DataFrame({"tweets":tweets,"pos":pos_sent,"neg":neg_sent})
        x_train,x_test,y_train,y_test=train_test_split(buffer_df.values,np.array(labels),random_state=2,train_size=0.9)
        vectorized_x_train=self.vectorizer.fit_transform(x_train[:,0])
        vectorized_x_test=self.vectorizer.transform(x_test[:,0])
        self.model.fit(vectorized_x_train,y_train)
        self.sentiment_model.fit(x_train[:,1:],y_train)
        dump(self.model,'./rf.joblib')
        dump(self.sentiment_model,'sentiment_model.joblib')
        pickle.dump(self.vectorizer,open('vectorizer.b','wb'))
        
    def predict(self,tweet):
        tweet=[tweet]
        pos,neg=self.find_sentiments(tweet)
        print(pos,neg)
        self.preprocess(tweet)
        tweet= self.vectorizer.transform(tweet)
        model_pred=self.model.predict(tweet)
        model_sent_pred=self.sentiment_model.predict(pd.DataFrame({"pos":pos,"neg":neg}).values)
        return model_pred,model_sent_pred