import csv
import pickle
import pandas as pd

def find_list(categories):
    with open('food.pickle', 'rb') as f:
        food_dict = pickle.load(f)
    print("food_dict assembled")

    with open('restaurant.pickle', 'rb') as g:
        restaurant_dict = pickle.load(g)
    print("restaurant_dict assembled")

    category_list = food_dict[categories[0]]
    for a_category in categories:
        category_list = [x for x in category_list if x in food_dict[a_category]]
    print(len(category_list))
    restaurant_list = []

    for UID in category_list:
        restaurant = restaurant_dict[UID]
        restaurant_list.append(restaurant)


    return restaurant_list

def get_categories():
    with open('food.pickle', 'rb') as f:
        food_dict = pickle.load(f)
    print("food_dict assembled")

    return list(food_dict.keys())
