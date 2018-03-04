import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import business_dataframe
import retrieve_list

def construct_keywords(name):
    '''
    Input:
        name: a string
    Output:
        namelist: a list of possible formats of name. namelist should have length 4.
    '''
     
    nameset = set()
    # itself, no space, hashtags, lowercase
    nameset.add(name)
    # remove possible whitespace
    name_nospace = name.replace(" ", "")
    nameset.add(name_nospace)
    nameset.add('@'+name_nospace)
    # hashtage + capital initials
    nameset.add('#'+name_nospace)
    # hashtage + lowercase
    nameset.add('#'+name_nospace.lower())
    
    return list(nameset)


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
    
    colnames = ("rname", "text","retweet_count","favorite_count", "followers", "sentiment", "score")
    df = pd.DataFrame(columns=colnames)
    
    tweets_file = open(path, "r")
    
    l = 0 # restaurants matched
    for line in tweets_file:
    
        try:
            tweet = json.loads(line)
            
            # whether a tweet is a retweet
            is_retweet = re.search("^RT",tweet['text'])
            
            for i in namedict:
                possible_names = namedict[i]
                
                if is_retweet:
                    # whether is a extended text
                    if 'extended_tweet' in tweet['retweeted_status']:
                        match = re.search(r"(?=("+'|'.join(possible_names)+r"))",\
                                          tweet['retweeted_status']['extended_tweet']['full_text'])
                    else:
                        match = re.search(r"(?=("+'|'.join(possible_names)+r"))",tweet['text'])
                else:
                    # whether is a extended text
                    if 'extended_tweet' in tweet:
                        match = re.search(r"(?=("+'|'.join(possible_names)+r"))",\
                                          tweet['extended_tweet']['full_text'])
                    else:
                        match = re.search(r"(?=("+'|'.join(possible_names)+r"))",tweet['text'])
                
                    
                if match:
                    l += 1
                    
                    if is_retweet:
                        twinfo = calculate_score(i, tweet, True)
                    else:
                        twinfo = calculate_score(i, tweet)
                    
                    #print('\n',twinfo)
                    df_temp = pd.DataFrame(twinfo, columns=colnames)
                    #print(df_temp)
                    df = df.append(df_temp, ignore_index=True)
                    
                    
                    break
                
        except:
            #print('Failed: ', str(e))
            continue
    
    print('twitter scanning finished')
    print('# matches:', l)
    return df
  

                  
def calculate_score(i, tweet, is_retweet=False):
    analyzer = SentimentIntensityAnalyzer()
    
    retweet = tweet['retweet_count']
    likes = tweet['favorite_count']
    followers = tweet['user']['followers_count']
    
    if is_retweet:
        if 'extended_tweet' in tweet['retweeted_status']:
            senti_score = float(analyzer.polarity_scores(tweet['retweeted_status']['extended_tweet']['full_text'])['compound'])
            text = tweet['retweeted_status']['extended_tweet']['full_text']
        else:
            senti_score = float(analyzer.polarity_scores(tweet['text'])['compound'])
            text = tweet['text']
    else:
        if 'extended_tweet' in tweet:
           senti_score = float(analyzer.polarity_scores(tweet['extended_tweet']['full_text'])['compound'])
           text = tweet['extended_tweet']['full_text']
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
        i_mean = round(i_mean, 4)
        ranking.append((i, i_mean))

    # sort the ranking in decreasing order
    merge_sort(ranking)
    
    return ranking
           



if __name__ == '__main__':
    category_list = 'pizza'
    business_dataframe.dict_assemble("pickle")
    
    raw_list = retrieve_list.find_list(category_list)
    
    # get a list of names
    res_list = raw_list[1]
    print(len(res_list))
    print()
    
    
    tweets_data_path = './twitter_data3.txt'
    # example
    #res_list = ['Lou Malnati\u2019s', 'Pablo Fransico','SLU']
    res_dict = dict_converter(res_list[:100])
    
    df = read_data(tweets_data_path, res_dict)
    print(df.rname.value_counts())
    rank = analyze_df(df)
    
    for i in rank:
        print(i)
    
    
    
