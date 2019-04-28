import mysql.connector as mysql
import pandas as pd
class MysqlBackendConnector:
    def __init__(self,dbname,user,password):
        self.db=mysql.connect(host="localhost",user=user,passwd=password,database=dbname)
    def insert_tweets(self,tweet_category_pairs):
        cursor=self.db.cursor()
        query="INSERT INTO tweets_log VALUES(%s,%s)"
        cursor.executemany(query,tweet_category_pairs)
        self.db.commit()
    def retrieve_tweets(self):
        cursor=self.db.cursor()
        query="SELECT * FROM tweets_log"
        cursor.execute(query)
        tweets=cursor.fetchall()
        tweets_,categories=[t[0] for t in tweets],[t[1] for t in tweets]
        return pd.DataFrame({"Tweets":tweets_,"Categories":categories})
    def reset_table(self):
        query ="DELETE FROM tweets_log"
        cursor= self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        