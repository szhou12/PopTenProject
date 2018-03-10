import pandas as pd
from .util import analysis2
from .util import business_dataframe
from .util import retrieve_list
from .util import googlemap
import os

TWEETS_PATH = './twitter_data12.txt'

def get_address(yelp_dict, restaurant_name):
    '''
    get a restaurant's address (street, city, state)
    Input:
        yelp_dict: (dictionary) yelp dictionary that mappes a restaurant name to its information
        restaurant_name: (str) a given name
    Output:
        rv (str): given restaurant's address
    '''
    info_list = yelp_dict[restaurant_name]
    address = info_list[:3]
    rv = ', '.join(address)
    return rv

def get_tweet(twi_df, restaurant_name):
    '''
    Get a tweet about a restaurant. This tweet has the highest score.
    Input:
        twi_df: pandas dataframe that contains proper tweets information
        restaurant_name: (str) a given name
    Output:
        text: (str) tweet content
    '''
    filter_df = twi_df[twi_df['rname']==restaurant_name]
    #text = filter_df.iloc[0]['text']
    text = filter_df.loc[filter_df['score'].idxmax()]['text']
    return text

def get_format(rank, twi_df, yelp_dict):
    '''
    context format to render
    Inputs:
        rank: a list of tuples (restaurant_name, twitter_score)
        twi_df: dataframe for matched restaurants.
        yelp_dict: dictionary about each restaurant's info in Yelp.
    Output:
        output: dictionary
    '''
    rank = rank[:10]
    output = {}
    l = len(rank)


    for i in range(l):
        res_name = rank[i][0]
        
        output['Restaurant'+str(i+1)] = res_name
        output['Address'+str(i+1)] = get_address(yelp_dict, res_name)
        output['Tweet'+str(i+1)] = get_tweet(twi_df, res_name)
        output['yscore'+str(i+1)] = yelp_dict[res_name][3]
        output['tscore'+str(i+1)] = rank[i][1]

    if l < 10:
        for i in range(l+1, 11):
            output['Restaurant'+str(i+1)] = ''
            output['Address'+str(i+1)] = ''
            output['Tweet'+str(i+1)] = ''
            output['yscore'+str(i+1)] = ''
            output['tscore'+str(i+1)] = ''
            
    return output
            
            
        


def main_algorithm(data):
    '''
    Combine all info from Yelp and Twitter. Render a proper result to Django.
    Input:
        data: Django data
        tuple: (boolean, context)
    '''

    food_type = data['food_type']
    origin = data['address']
    city = data['city']

    business_dataframe.dict_assemble("pickle")
    raw_tuple = retrieve_list.find_list(food_type)
    raw_dict = raw_tuple[0]
    raw_list = raw_tuple[1]
    
    res_dict, city_list, id_list = analysis2.dict_converter(raw_dict, raw_list, city, food_type)

    geocode_origin = googlemap.get_geocode(origin)

    if not res_dict:
        context = {'error': 'Sorry we can\'t find results for your input. Please try again'}
        return (False, context)
    elif geocode_origin[0] != 'ROOFTOP':
        context = {'error': 'Sorry your location is too obscure. Please try again'}
        return (False, context)
    else:
        df = analysis2.read_data(TWEETS_PATH, res_dict, city_list, id_list)
        if df.empty:
            context = {'error': 'Sorry our dataset has no results'}
            return (False, context)
        else:
            rank = analysis2.analyze_df(df)
            context = get_format(rank, df, raw_dict)
            context['OriginCoords'] = geocode_origin[1]
            context['OriginAddress'] = geocode_origin[2]
            
            print('Processed successfully. Ready to render.')
            return (True, context)

    
    
