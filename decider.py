import pandas as pd
import spacy
import string
import numpy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB,GaussianNB,ComplementNB,BernoulliNB
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
from sklearn.svm import SVC,NuSVC
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier
from joblib import dump, load
import pickle


nlp=spacy.load('en_core_web_sm')
class Decider:
    def __init__(self,mode="test"):
        if mode == 'train':
            self.model= RandomForestClassifier(n_estimators=250,criterion='entropy',verbose=10,random_state=3,n_jobs=-1,oob_score=True,)
            #self.model = MultinomialNB()
            self.vectorizer = TfidfVectorizer(min_df=3)
        else:
            self.model= load('rf_.joblib')
            self.vectorizer= pickle.load(open('vectorizer_.b','rb'))
            
            
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
        self.preprocess(tweets)
        x_train,x_test,y_train,y_test=train_test_split(tweets,labels,random_state=2,train_size=0.9)
        x_train=self.vectorizer.fit_transform(x_train)
        x_test=self.vectorizer.transform(x_test)
        self.model.fit(x_train,y_train)
        dump(self.model,'./rf_.joblib')
        pickle.dump(self.vectorizer,open('vectorizer_.b','wb'))
        
    def predict(self,tweet):
        #tweet=[tweet]
        self.preprocess(tweet)
        tweet= self.vectorizer.transform(tweet)
        return self.model.predict(tweet)
