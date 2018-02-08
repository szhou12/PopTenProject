#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:32:52 2018

@author: JoshuaZhou
"""


# import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# user credentials to access Twitter API
consumer_key = 'OPpDRcG6pA4DOlSXHhWWhW9ng'
consumer_secret = '6wAO1jrCt89a00ghETQRbAlnicPn8jn6QGcVK2c0AdAk6HbIlc' 
access_token = '960985220131508224-PQ6rSxg5WuEQSyEVbGttM8Lu4DuafYG'
access_token_secret = '6xP3UICqaN7ngLF5IjR37iAoNqZxYrcSNBIwUNeQcmdBV'

class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True
#    def on_error(self, status):
#        print(status)
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

class identity(object):
    def __init__(self, name):
        self.all_tweets = []
        self.name = name
    
    def get_name(self):
        return self.name
          
    def set_name(self, n):
        self.name = n
    
    def append_tweet(self, t_obj):
        self.all_tweets.append(t_obj)
    
    

class txt_attributes(object):
    def __init__(self):
        self.content = None
        self.sentiment = None
        self.favorite_count = None
        self.retweet_count = None
        
    @property
    def content(self):
        return self._content
    @property
    def sentiment(self):
        return self._sentiment
    @property
    def favorite_count(self):
        return self._favorite_count
    @property
    def retweet_count(self):
        return self._retweet_count
    
    
    @content.setter
    def content(self, content):
        self._content = content
    @sentiment.setter
    def sentiment(self, sentiment):
        self._sentiment = sentiment
    @favorite_count.setter
    def favorite_count(self, favorite_count):
        self._favorite_count = favorite_count
    @retweet_count.setter
    def retweet_count(self, retweet_count):
        self._retweet_count = retweet_count
    
def sentianalysis(tweet_text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(tweet_text)
    return "{:-<65} {}".format(tweet_text, str(vs))

def find_tweets(database):
    '''
    This funciton takes a database (either in Pandas or SQL) for a list of restaurant names,
    finds the all tweets for each restaurant and does the sentiment analysis.
    '''
    # set up listener
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    
    # filter
    for i in database:
        r = identity(i)
        
        l = stream.filter(track=[i], async=True)
        # need a panda frame rather than filter
        
        for tweet in l:
            a = txt_attributes()
            a.content = tweet.text
            a.sentitment = sentianalysis(tweet.text)
            a.favorite_count = tweet.favorite_count
            a.retweet_count = tweet.retweet_count
            r.append_tweet(a)
    
    
    
    
    
    
    
    
    
    
    
    