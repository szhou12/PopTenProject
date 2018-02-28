import pandas as pd
import pickle
import csv

def dict_assemble(save_format, constraint = False):
    businesses_df = pd.read_json('business.json', lines = True, encoding = "utf-8")

    iterator = 0

    restaurant_dict = dict()
    food_dict = dict()
    city_set = set()

    for row in businesses_df.itertuples():
        if row.is_open == 1 and 'Restaurants' in row.categories:
            business_name = row.name
            address = row.address
            city = row.city
            state = row.state
            if constraint != False:
                if state != constraint:
                    continue
            city_set.add(city)
            stars = row.stars
            categories = row.categories
            latitude = row.latitude
            longitude = row.longitude
            iterator += 1
            UID = iterator
            for cuisine in categories:
               if cuisine in food_dict:
                   food_dict[cuisine].append(UID)
               else:
                   food_dict[cuisine] = [UID]
            restaurant_dict[UID] = [business_name, address, city, state, stars, (longitude, latitude)]
            print(UID)
    if save_format == 'csv':
        restaurant_headers = restaurant_dict.keys()
        food_headers = food_dict.keys()
        with open("restaurant.csv", "w", encoding = "utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(restaurant_headers)
            writer.writerows(zip(restaurant_dict.values()))
        with open("food.csv", "w", encoding = "utf-8") as g:
            writer = csv.writer(g)
            writer.writerow(food_headers)
            writer.writerows(zip(food_dict.values()))
    elif save_format == 'pickle':
        with open('restaurant.pickle', 'wb') as f:
            pickle.dump(restaurant_dict, f)
        with open('food.pickle', 'wb') as g:
            pickle.dump(food_dict, g)
    with open("Cities.txt", "w") as h:
        h.write(str(city_set))
        
    return "Finished"


               
           
        
