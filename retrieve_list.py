import csv
import pickle
import pandas as pd
from itertools import combinations

def find_list(strings):
    strings = strings.title()
    categories = [word.strip() for word in strings.split(',')]
    with open('food.pickle', 'rb') as f:
        food_dict = pickle.load(f)
    print("food_dict assembled")

    with open('restaurant.pickle', 'rb') as g:
        restaurant_dict = pickle.load(g)
    print("restaurant_dict assembled")

    exception_string = ''
    categories_cleaned = []
    
    for a_category in categories:
        try:
            UID_list = food_dict[a_category]
        except KeyError:
            if exception_string == '':
                exception_string = "We could not find restauraunts matching"
            else:
                exception_string = exception_string + ","
            exception_string = exception_string + " " + a_category
            continue
        categories_cleaned.append(a_category)

    category_combinations = []
    if len(categories_cleaned) == 2:
        category_combinations += ([list(y) for y in combinations(categories_cleaned, 1)])
        category_combinations += [categories_cleaned]
    elif len(categories_cleaned) > 2:
        for x in range (2, len(categories_cleaned) + 1):
            category_combinations += ([list(y) for y in combinations(categories_cleaned, x)])
    else:
        category_combinations = [categories_cleaned]

    category_dict = dict()
    for a_list in category_combinations:
        category_list = []
        for a_category in a_list:
            if category_list == []:
                category_list = food_dict[a_category]
            else:
                category_list = [x for x in category_list if x in food_dict[a_category]]
        restaurant_list = []
        for UID in category_list:
            restaurant = restaurant_dict[UID]
            restaurant_list.append(restaurant)
        category_dict[str(a_list)] = restaurant_list

    next_best_string = ''
    if len(categories_cleaned) > 1:
        value_length = list(category_dict.values())
        value_length = [len(x) for x in value_length]
        keys = list(category_dict.keys())
        maximum = keys[value_length.index(max(value_length))]
        if category_dict[maximum] != category_dict[str(categories_cleaned)]:
            next_best = maximum
            next_best_string = "We also found " + str(len(category_dict[maximum])) + " results for " + next_best

            
    return category_dict[str(categories_cleaned)], next_best_string, exception_string

def get_categories():
    with open('food.pickle', 'rb') as f:
        food_dict = pickle.load(f)
    print("food_dict assembled")

    return list(food_dict.keys())
