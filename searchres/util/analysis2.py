import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import os
import jellyfish

#import business_dataframe
#import retrieve_list


def construct_keywords(name, is_restaurant=False):
    '''
    Given a restaurant's full name, construct possible forms of the name written in the tweet
    Inputs:
        name: a string
        is_restaurant: (Boolean) if True then do fomatting according to restaurant name
    Output:
        namelist: a list of possible formats of name. namelist should have length 4.
    '''
     
    nameset = set()
    nameset.add(" "+name+" ") # e.g." lou Manti's "

    name_nospace = name.replace(" ", "") 
    nameset.add(" "+name_nospace+" ") # e.g." louManti's "

    if not is_restaurant:
        nameset.add(name_nospace.lower())
        
    if "'" in name_nospace:
        name_nospace = name_nospace.replace("'", "")
        
    if is_restaurant:
        nameset.add('@'+name_nospace) # e.g. "@louMantis"
    
    nameset.add('#'+name_nospace) # e.g. "#louMantis"
                
    nameset.add('#'+name_nospace.lower()) # e.g. "#loumantis"
    
    return list(nameset)


def dict_converter(dic, lst, city, foodtype):
    '''
    clean the yelp list by filtering by a given city
    Inputs:
        dic: yelp dictionary that mappes a restaurant name to its information
        lst: list of restaurant names filtered by a given food type
        city: user's specified city name
        foodtype: (str) user's specified food type
    Output:
        rv: (dictionary) it contains all restaurants in Yelp that have a specified food type in a given city
        city_list: (list) all possible names of a city
        identifiers: (list) attributes help to identify restaurant name in a tweet e.g. food type attribute
    '''
    # city may be a wrong word
    city = city.title()
    rv = {}
    for i in lst:
        if dic[i][1] == city:
            ilst = construct_keywords(i, True)
            rv[i] = ilst

    # get all possible forms of a city name
    city_list = construct_keywords(city)

    # possible attributes to filter tweets
    attrs = [foodtype] + ['food'] + ['restaurant']
    identifiers = []
    for k in attrs:
        temp = construct_keywords(k)
        identifiers += temp
        
    return rv, city_list, identifiers


def get_tweet_text(tweet, is_retweet):
    '''
    Whether a given tweet is a retweet.
    Get the tweet text accordingly.
    Inputs:
        tweet: raw tweet
        is_retweet: boolean
    Output:
        text: (String) tweet contents
    '''
    if is_retweet:
        # whether is a extended text
        if 'extended_tweet' in tweet['retweeted_status']:
            text = tweet['retweeted_status']['extended_tweet']['full_text']
        else:
            text = tweet['text']
            
    else:
        # whether is a extended text
        if 'extended_tweet' in tweet:
            text = tweet['extended_tweet']['full_text']
        else:
            text = tweet['text']
    
    return text
    


def read_data(path, namedict, city_list, id_list):
    '''
    Read in twitter data and build up the pandas dataframe with twitter data we need
    Input:
        path: path access to the raw twitter data
        namedict: a dictionary of restaurant names
        city_list: a list of all possible forms of a given city
        id_list: a list of identifies from the function dict_converter()
    Output:
        df: built-up pandas dataframe
    '''
    
    colnames = ("rname", "text","retweet_count","favorite_count", "followers", "sentiment", "score")
    df = pd.DataFrame(columns=colnames)

    script_dir = os.path.dirname(__file__)
    tweets_file_path = os.path.join(script_dir, path)
    
    tweets_file = open(tweets_file_path, "r")
    
    l = 0 # restaurants matched
    for line in tweets_file:
    
        try:
            tweet = json.loads(line)
            
            # whether a tweet is a retweet; retweet starts with RT
            is_retweet = re.search("^RT",tweet['text'])
            
            for i in namedict: # i -- a restaurant
                possible_names = namedict[i]
                
                text = get_tweet_text(tweet, is_retweet)
                text = " "+text+" "
                
                match_list = [m for m in possible_names if m in text]
                has_attrs = [attr for attr in id_list if attr in text]
                if city_list:
                    has_city = [c for c in city_list if c in text]
                    
                if match_list and has_attrs:
                    l += 1
                    
                    if is_retweet:
                        twinfo = calculate_score(i, tweet, match_list, has_city, True)

                    else:
                        twinfo = calculate_score(i, tweet, match_list, has_city)
                    

                    df_temp = pd.DataFrame(twinfo, columns=colnames)
                    df = df.append(df_temp, ignore_index=True)
                        
                    break
                
        except:
            #print('Failed: ', str(e))
            continue
    
    print('twitter scanning finished')
    print('# matches:', l)
    return df
  
def calculate_prob(text, match):
    '''
    This function calculates the likelihood of a single tweet being about a restaurant.
    The reason of computing probability is that given a restaurant name form (#PINO)
    It could be the case that a tweet wrote as #PINOisadog.
    We count this tweet is a match but we are not 100% sure. So instead we compute
    the jaro_winkler value of ("#PINO", "#PINOisadog") as the probabilty that this tweet
    is actually about the restaurant. 
    We get cumulative probabilities and return its mean at the end.
    Inputs:
        text: (string) tweet text
        match: (list of strings) all possible forms of a restaurant name found matched in the tweet
    Output:
        probability: (float) the probability that this tweet is about the given restaurant
        
    '''
    
    counter = 0
    tot = 0
    if match: # not empty list
        for i in match:
            score_set = set()
            n = len(i.split())
            if n == 1:
                i = i.split()[0] # get rid of outer spaces
                for j in text.split():
                    if i in j:
                        cur_score = jellyfish.jaro_winkler(i,j)
                        score_set.add(cur_score)

            else:
                # text splited in the group of n
                pieces = text.split()
                reformed_text_split = [" ".join(pieces[k:k+n]) \
                                       for k in range(0, len(pieces))]
                i = ' '.join(i.split()) # get rid of outer spaces
                for j in reformed_text_split:
                    if i in j:
                        cur_score = jellyfish.jaro_winkler(i,j)
                        score_set.add(cur_score)
                        
            tot += max(score_set)
            counter += 1

        return tot/counter
    else:
        return 0
                    
            
                  
def calculate_score(i, tweet, match_list, has_city, is_retweet=False):
    '''
    Calculate the expected score of a single tweet
    Formula: [(retweets + likes + followers)*sentimental_score] * probability
    Inputs:
        i: current restaurant name
        tweet: current tweet being processed
        match_list: a list of possible forms of restaurant names found matched in the tweet
        is_retweet: (Boolean) is this tweet a retweet
        
    Output:
        twinfo: all tweet info ready to be appended to Pandas
          
    '''
    analyzer = SentimentIntensityAnalyzer()
    
    retweet = tweet['retweet_count']
    likes = tweet['favorite_count']
    followers = tweet['user']['followers_count']
    
    text = get_tweet_text(tweet, is_retweet)
    senti_score = float(analyzer.polarity_scores(text)['compound'])
    
    # probability of a single tweet
    probability = calculate_prob(text, match_list)

    if has_city:
        city_prob = calculate_prob(text, has_city)
    else:
        # city name not shown in the tweet
        city_prob = 0.5
        
    
    # score of a single tweet: x*P(x)
    tot_score = (retweet + likes+ followers)*senti_score * probability * city_prob

    
    twinfo = [(i, text, retweet, likes, followers, senti_score, tot_score)]
        
    return twinfo





def merge_sort(lst):
    '''
    sort in decreasing order
    Input:
        lst: a list
    Output:
        a sorted list
    '''
    if len(lst) > 1:
        mid = len(lst)//2
        l_half = lst[:mid]
        r_half = lst[mid:]

        merge_sort(l_half)
        merge_sort(r_half)

        i=0
        j=0
        k=0
        while i < len(l_half) and j < len(r_half):
            if l_half[i][1] > r_half[j][1]:
                lst[k]=l_half[i]
                i=i+1
            else:
                lst[k]=r_half[j]
                j=j+1
            k=k+1

        while i < len(l_half):
            lst[k]=l_half[i]
            i=i+1
            k=k+1

        while j < len(r_half):
            lst[k]=r_half[j]
            j=j+1
            k=k+1
    else:
        return

def analyze_df(obj_df):
    '''
    analyze the pandas dataframe that contains information for all searched objects
    Input:
        obj_df: pandas dataframe
    Output:
        ranking: a list of tuples sorted in decreasing order
    '''
    # construct a list of tuples
    ranking = []
    for i, i_df in obj_df.groupby('rname'):
        exp_value_i = i_df.score.sum()
        exp_value_i = round(exp_value_i, 1)
        ranking.append((i, exp_value_i))

    # sort the ranking in decreasing order
    merge_sort(ranking)
    
    return ranking
           

