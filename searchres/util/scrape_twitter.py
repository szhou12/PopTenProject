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
import os
import json

consumer_key = 'OPpDRcG6pA4DOlSXHhWWhW9ng'
consumer_secret = '6wAO1jrCt89a00ghETQRbAlnicPn8jn6QGcVK2c0AdAk6HbIlc' 
access_token = '960985220131508224-PQ6rSxg5WuEQSyEVbGttM8Lu4DuafYG'
access_token_secret = '6xP3UICqaN7ngLF5IjR37iAoNqZxYrcSNBIwUNeQcmdBV'

FILENAME = './business.json'

def get_all_names(filename, cutoff):
    '''
    Get all category names in Yelp that have "Restaurants" in "categories" attribute
    Input:
        filename: (str) filename of yelp dataset
    Output:
        a list of all categories in Yelp dataset
    '''
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    yelp_file = open(file_path, "r")
    select_categories = set()
    freq = {}
    for line in yelp_file:
        try:
            aRestaurant = json.loads(line)
            if 'Restaurants' in aRestaurant["categories"]:
                cate = aRestaurant['categories']
                for i in cate:
                    if i in freq:
                        freq[i] += 1
                    else:
                        freq[i] = 1
                    
        except BaseException as e:
            print('Failed: ', str(e))
            continue
    
    for i in freq:
        if freq[i] >= cutoff:
            if "&" in i:
                # case: 'Coffee & Tea'
                i = i.split(" & ") #  a list
                for k in i:
                    select_categories.add(k)
            elif "(" in i and ")" in i:
                # case: 'American (Traditional)'
                start = i.find(" (")
                end = i.find(")")
                temp = i.replace(i[start:end+1],"")
                select_categories.add(temp)
            else:
                select_categories.add(i)
            

    select_names = set(select_categories)

    return list(select_names)


def construct_keywords(name):
    '''
    Input:
        name: a string 
        is_restaurant: (Boolean) True if 'name' is a restaurant name; False otherwise
    Output:
        namelist: a list of possible formats of name.
    '''
    nameset = set()
    # itself, no space, hashtags, lowercase
    nameset.add(name)
    # remove possible whitespace
    name_nospace = name.replace(" ", "")
    nameset.add(name_nospace)
    
    # hashtage + capital initials
    nameset.add('#'+name_nospace)
    # hashtage + lowercase
    nameset.add('#'+name_nospace.lower())
                
    
    return list(nameset)

class StdOutListener(StreamListener):
    '''
    Tweepy Listener
    '''

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
    r_namelst = []
    cutoff = 300
    
    adjlst = ["Restaurant", "Food", "Food Porn", "Foodie", "Yummy", "Tasty",\
              "Delicious", "Savory", "Divine"]
    namelst = get_all_names(FILENAME, cutoff)
    sumlst = adjlst + namelst
    for loc in sumlst:
        loclist = construct_keywords(loc) 
        r_namelst += loclist
        
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode='extended') 

    stream.filter(track=r_namelst)
    
