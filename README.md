# PopTen: A CSS122 Project

## Synopsis
The goal of our project is to collect data from the social media Twitter, in order to interpret this information to predict the trends of restaurants within a specific location.  We foresee the creation of a website from which we will be able to provide users the ability to select from search criteria, including location and food type, and be returned information on restaurants that have been popular among twitter users in the area in order to provide useful suggestions and directions to those restaurants.

## Getting Started
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
- Step 7: Open 'main_algorithm.py' in Python editor, find 'TWEETS_PATH' and replace its assigned value with your twitter_data filename

### DIY: Set up the cutoff for keywords
**If you want to decide what keywords will be used to filter tweets, you can follow the steps shown below:**
- Step 1: Go to $PopTenProject/searchres/util/
- Step 2: Open 'scrape_twitter.py' in Python editor and find __main__
- Step 3: find 'cutoff' variable and replace its assigned value with the one you want
- Note: 'cutoff' decides what restaurant categories/food types in Yelp dataset will be included into the keywords list for filtering tweets.
E.g. if cutoff = 300, and 'pizza' is a category that appears over 300 times in Yelp dataset, then 'pizza' will be included into the keywords list for filtering tweets. 
- Note: Generally, we want as many keywords as possible (set cutoff as low as possible) to include every restaurant category/food type. But that will increase the time of scraping data. Therefore, mind that there is a tradeoff between shoretening the time of scraping and lowering the cutoff.

### PopTen Website Handbook
- **Step 1**: Once you open our website, you will be provided 3 search bars:
- 'Food Type' allows you to enter a food type you want to search (e.g. 'pizza', 'burger', 'bars')
- 'City' specifies the location of restaurants you want to search
- 'Location' allows you to enter your current location 
- Note: the 'Location' input doesn't have to be as detailed as a formatted address, but it needs to be more specific than 'City'
- **Step 2**: Hit the search button, and wait.
- Note: It takes around 5 minutes or more to run the program (depending on your input and the size of twitter dataset)
- **Step 3**: The results will be shown in a list, each with a drop-down menu and in a map
- Note: In the map, the start is your current location, and you can choose an end in the drop-down menu. You can also choose a travel mode. Then the map will show you the route.

## Code Structure
**Main funcions under PopTenProject/searchres**
- main_algorithm.py: integrated function linked to front-end
- /util/scrape_twitter.py: Twitter data scraper
- /util/analysis2.py: combine information from both Yelp and twitter and conduct the analysis (See details in PopTenProject/Documents/
- /util/business_dataframe.py: combine with retrieve_list.py to extract Yelp data filtered by food type 
- /util/retrieve_list.py: same as above

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

## Source
- [freemiumdownload](http://freemiumdownload.com/demo?theme=bootstrap-coffee-pizza) - The web framework modified and used
