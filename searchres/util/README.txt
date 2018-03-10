In order to analyze datasets, please add the following files into this folder:

"business.json"

[twitter_data filename] (Note: this should be the name of twitter dataset you scraped using scrape_twitter.py. e.g. "twitter_data12.txt") 


Note: 

1. If you have a different twitter_data filename than the one we previously set up, please go to main_algorithm.py, find TWEETS_PATH and substitute the default filename with the one you want to use.  

2. Scraping Twitter data DIY: Turn on the terminal, go to the directory where the util folder is at, find scrape_twitter.py and run the following script command: 

python scrape_twitter.py > [twitter_data filename] (better save it as a txt file)