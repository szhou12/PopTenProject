import business_dataframe
import retrieve_list
import analysis2

TWEETS_PATH = './twitter_data3.txt'

def get_format(rank, twi_df, string_tuple):
    rank = rank[:10]
    output = {}
    l = len(rank)
    
    output['String1'] = string_tuple[0]
    output['String2'] = string_tuple[1]

    for i in range(l):
        output['Restaurant'+str(i+1)] = rank[i][0]
        filterdf = twi_df[twi_df['rname']==rank[i][0]]
        output['Tweet'+str(i+1)] = filterdf.iloc[0]['text']

    if l < 10:
        for i in range(l+1, 11):
            output['Restaurant'+str(i+1)] = ''

            output['Tweet'+str(i+1)] = ''
            
    return output
            
            
        


def main_algorithm(data):
    
    '''
    is_valid_data = check_input(data)
    '''


    food_type = data['food_type']
    address = data['address']
    city = data['city']

    business_dataframe.dict_assemble("pickle")
    raw_tuple = retrieve_list.find_list(food_type)

    raw_dict = raw_tuple[0]
    raw_list = raw_tuple[1]
    next_best = raw_tuple[2]
    exception_string = raw_tuple[3]
    string_tuple = (next_best, exception_string)
    
    res_dict = analysis2.dict_converter(raw_dict, raw_list, city)

    if not res_dict:
        context = {'error': 'Sorry we can\'t find results for your input. Please try again'}
        return (False, context)
    else:
        df = analysis2.read_data(TWEETS_PATH, res_dict)
        if df.empty:
            context = {'error': 'Sorry our dataset has no results'}
            return (False, context)
        else:
            rank = analysis2.analyze_df(df)
            context = get_format(rank, df, string_tuple)
            
            print('output: ', context)
            return (True, context)

    
    
