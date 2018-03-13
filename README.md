# PopTen: A CSS122 Project

## Synopsis
The goal of our project is to collect data from the social media website Twitter, in order to interpret this information to predict the trends of restaurants within a specific location.  We foresee the creation of a website from which we will be able to provide users the ability to select from search criteria, including location and food type, and be returned information on restaurants that have been popular among twitter users in the area in order to provide useful suggestions.

## Getting Started
- Step 1: Download the whole project, keep the order of files as it is shown in here.
- Step 2: Copy and paste Yelp dataset ('business.json') and Twitter dataset (e.g. 'twitter_data12.txt') into the folder named util.
- Step 3: Open the terminal, change the directory to where manage.py is at.
- Step 4: Run the following command:
```
python manage.py runserver
```
- Step 5: Wait util it shows a web address (e.g. http://127.0.0.1:8000/)
- Step 6: Copy and paste this address to your web browser
- Step 7: add 'poptenrestuarant' at the end to make it look as http://127.0.0.1:8000/poptenrestuarant/
- Step 8: You have our website ready to go!

## Installation
**Python packages required:**
- tweepy == 3.6.0
- pandas >= 0.22.0
- googlemaps
- vadersentiment
- jellyfish
- json
- Django == 2.0.2
- django-form
