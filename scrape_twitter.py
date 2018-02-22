#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 20:05:08 2018

@author: JoshuaZhou
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time

consumer_key = 'OPpDRcG6pA4DOlSXHhWWhW9ng'
consumer_secret = '6wAO1jrCt89a00ghETQRbAlnicPn8jn6QGcVK2c0AdAk6HbIlc' 
access_token = '960985220131508224-PQ6rSxg5WuEQSyEVbGttM8Lu4DuafYG'
access_token_secret = '6xP3UICqaN7ngLF5IjR37iAoNqZxYrcSNBIwUNeQcmdBV'


def construct_keywords(name):
    '''
    Input:
        name: a string
    Output:
        namelist: a list of possible formats of name. namelist should have length 4.
    '''
    # itself, no space, hashtags, lowercase
    namelist = [name]
    # remove possible whitespace
    name_nospace = name.replace(" ", "")
    namelist.append(name_nospace)
    # hashtage + capital initials
    namelist.append('#'+name_nospace)
    # hashtage + lowercase
    namelist.append('#'+name_nospace.lower())                 
    
    return namelist

class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            print(data)
            return(True)
            
        except BaseException as e:
            print('Failed: ', str(e))
            time.sleep(1)

    def on_error(self, status):
        print('Error: ', status)

if __name__ == '__main__':

    loc = "Chicago"
    loclist = construct_keywords(loc) 
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode='extended') 

    stream.filter(track=loclist)
