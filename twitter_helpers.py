import twitter
import re
import csv
from credentials import *


def generate_twitter_api():
    api = twitter.Api(consumer_key=twitter_consumer_key,
                      consumer_secret=twitter_consumer_secret,
                      access_token_key=twitter_access_token,
                      access_token_secret=twitter_access_token_secret)
    return api


def fetch_twitter_user_tweets(api, username):
    '''Returns the last 20 tweets by the user
    '''
    statuses = api.GetUserTimeline(screen_name=username)
    return [s.text for s in statuses]


def extract_tweet_links(tweet):
    regex_exp = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]\
      |(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(regex_exp, tweet)


def generate_twitter_urls(api, username):
    tweets = fetch_twitter_user_tweets(api, username)
    response = []
    for tweet in tweets:
        response += extract_tweet_links(tweet)
    return response


def parse_twitter_usernames():
    with open('sources/twitter.csv', 'rb') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        for line in csv_reader:
            username, domain = line
            yield username.strip(), domain.strip()
