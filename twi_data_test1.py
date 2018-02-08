#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 13:33:22 2018

@author: JoshuaZhou
"""

# import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

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

if __name__ == "__main__":
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    
    # this line filter Twitter Streams to capture data by the keywords:
    # 'restaurant'
    stream.filter(track=['restaurant'], async=True)