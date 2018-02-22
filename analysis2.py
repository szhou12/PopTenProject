import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import re

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


def word_in_text(wordlist, text):
    for word in wordlist:
        match = re.search(word, text)
        if match:
            return True
    
    return False

def dict_converter(lst):
    rv = {}
    for i in lst:
        ilst = construct_keywords(i)
        rv[i] = ilst
    return rv


def read_data(path, namedict):
    '''
    issue here is to find full_text because text can be truncated
    '''
    
    colnames = ("rname", "text","retweet_count","favorite_count", "reply_count","followers", "sentiment", "score")
    df = pd.DataFrame(columns=self.colnames)
    
    
    tweets_file = open(path, "r")
    
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            for i in namedict:
                possible_names = self.namedict[i]

                if retweeted_status in tweet:
                    match = re.search(r"(?=("+'|'.join(possible_names)+r"))",\
                                      tweet['retweeted_status']['extended_tweet']['full_text'])
                else:
                    match = re.search(r"(?=("+'|'.join(possible_names)+r"))",\
                                      tweet['text'])
                    
                if match:
                    if 'retweeted_status' in tweet:
                        twinfo = calculate_score(i, tweet, True)
                    else:
                        twinfo = calculate_score(i, tweet)

                    df_temp = pd.DataFrame(twinfo, columns=colnames)
                    df = df.append(df_temp, ignore_index=True)
                    break
        except BaseException as e:
            print('Failed: ', str(e))
            # wait for 1 sec
            time.sleep(1)

    return df
                    
def calculate_score(i, tweet, full=False):
    analyzer = SentimentIntensityAnalyzer()
    
    retweet = tweet['retweet_count']
    likes = tweet['favorite_count']
    followers = tweet['user']['followers_count']
    
    if full:
        senti_score = float(analyzer.polarity_scores(tweet['retweeted_status']['extended_tweet']['full_text'])['compound'])
        text = tweet['retweeted_status']['extended_tweet']['full_text']
    else:
        senti_score = float(analyzer.polarity_scores(tweet['text'])['compound'])
        text = tweet['text']
        
    tot_score = (retweet + likes+ followers)*senti_score
    twinfo = [(i, text, retweet, likes, followers, senti_score, tot_score)]
        
    return twinfo

def merge_sort(alist):
    '''
    sort in decreasing order
    '''
    if len(alist) > 1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        merge_sort(lefthalf)
        merge_sort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][1] > righthalf[j][1]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    else:
        return

def analyze_df(obj_df):
    '''
    analyze the pandas dataframe that contains information for all searched objects
    '''
    # construct a list of tuples
    ranking = []
    for i, i_df in obj_df.groupby('rname'):
        i_mean = i_df.score.mean()
        ranking.append((i, i_mean))

    # sort the ranking in decreasing order
    merge_sort(ranking)
    
    return ranking
           



if __name__ == '__main__':
    tweets_data_path = '../twitter_data2.txt'

    # example
    loc = "Chicago"
    res_list = ['MingHin Cuisine', 'Joy Yee Noodle', 'Kung Fu Tea', 'Go 4 Food']
    res_dict = dict_converter(res_list)
    df = read_data(tweets_data_path, res_dict)
    rank = analyze_df(obj_df)
    
    for i in rank:
        print(i)
    
