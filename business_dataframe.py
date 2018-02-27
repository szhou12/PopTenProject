import pandas as pd

def dict_assemble():

    businesses_df = pd.read_json('business.json', lines = True)

    iterator = 0

    restaurant_dict = dict()
    food_dict = dict()

    for row in businesses_df.iterrows():
        index, row = row
        print(row)
        if row['is_open'] == 1:
            iterator += 1
            business_name = row['name']
            address = row['address']
            city = row['city']
            stars = row['stars']
            categories = row['categories']
            UID = iterator
            for cuisine in categories:
               if cuisine in food_dict:
                   food_dict[cuisine].append(UID)
               else:
                   food_dict[cuisine] = [UID]
            restaurant_dict[UID] = [business_name, address, city, stars]

    return (restaurant_dict, food_dict)

               
           
        
