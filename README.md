# PopTen: A CSS122 Project

## Synopsis
The goal of our project is to collect data from the social media Twitter, in order to interpret this information to predict the trends of restaurants within a specific location.  We foresee the creation of a website from which we will be able to provide users the ability to select from search criteria, including location and food type, and be returned information on restaurants that have been popular among twitter users in the area in order to provide useful suggestions and directions to those restaurants.

## Getting Started
### Run the project
- Step 1: Download the whole project, keep the order of files as it is shown in here
- Step 2: Copy and paste Yelp dataset ('business.json') and Twitter dataset (e.g. 'twitter_data12.txt') into the folder /util
- Step 3: Open the terminal, change the directory to where manage.py is at
- Step 4: Run the following command:
```
python manage.py runserver
```
- Step 5: Wait util it shows a web address (e.g. http://127.0.0.1:8000/)
- Step 6: Copy and paste this address to your web browser
- Step 7: Add 'poptenrestuarant' at the end to make it look as http://127.0.0.1:8000/poptenrestuarant/
- Step 8: You have our website ready to go!

### Installation
**Python packages required:**
- tweepy == 3.6.0
- pandas >= 0.22.0
- googlemaps
- vadersentiment
- jellyfish
- json
- Django == 2.0.2
- django-form

### DIY: Scraping your own twitter dataset
**If you want to create your own twitter dataset rather than use the default one, you can follow the steps shown below:**
- Step 1: Open the terminal, change the directory to $PopTenProject/searchres/util/
- Step 2: Check if 'scrape_twitter.py' is in the /util folder
- Step 3: Run the following command:
```
python scrape_twitter.py > [twitter_data filename]
```
e.g. twitter_data12.txt (better save it as .txt file to avoid any conflicts that may arise)
- Step 4: Wait for 2-3 hours to have a reasonably large dataset
- Step 5: Check if your dataset is in /util folder
- Step 6: If it is, change the directory to $PopTenProject/searchres/ and find 'main_algorithm.py'
- Step 7: Open 'main_algorithm.py' in Python editor and find 'TWEETS_PATH' and replace its assigned value wity your twitter_data filename

### DIY: Set up the cutoff for keywords
**If you want to decide what keywords will be used to filter tweets, you can follow the steps shown below:**
- Step 1: Go to $PopTenProject/searchres/util/
- Step 2: Open 'scrape_twitter.py' in Python editor and find __main__
- Step 3: find 'cutoff' variable and replace its assigned value with the one you want
- Note: 'cutoff' decides what restaurant categories/food types in Yelp dataset are included into the keywords list for filtering tweets
e.g. if cutoff = 300, and 'pizza' is a category that appears over 300 times in Yelp dataset, then 'pizza' will be included into the keywords list for filtering tweets. 
- Note: Generally, we want as many keywords as possible (set cutoff as low as possible) to include every restaurant category/food type. But that will increase the time of scraping data. Therefore, mind that there is a tradeoff between decreasing time of scraping and lowering the cutoff.

## Contributions and Responsibilities
**Shuyu Zhou**
- PopTenProject/searchres/main_algorithm.py
- PopTenProject/searchres/util/analysis2.py
- PopTenProject/searchres/util/googlemap.py
- PopTenProject/searchres/util/scrape_twitter.py
- PopTenProject/searchres/templates/temp.html
- PopTenProject/searchres/templates/noresults.html
- PopTenProject/searchres/templates/results.html
- PopTenProject/searchres/templates/index.html (modified)

**Ke Duan**
- PopTenProject/searchres/admin.py
- PopTenProject/searchres/apps.py
- PopTenProject/searchres/forms.py
- PopTenProject/searchres/models.py
- PopTenProject/searchres/tests.py
- PopTenProject/searchres/views.py
- PopTenProject/searchres/templates/index.html (modified)
- PopTenProject/manage.py
- PopTenProject/pptn/settings.py
- PopTenProject/pptn/urls.py
- PopTenProject/pptn/wsgi.py

**Andrew Deng**
- PopTenProject/searchres/util/business_dataframe.py
- PopTenProject/searchres/util/retrieve_list.py
