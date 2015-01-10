import twitter
import re
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


def generate_twitter_link_batch(username):
    api = generate_twitter_api()
    tweets = fetch_twitter_user_tweets(api, username)
    response = []
    for tweet in tweets:
        response += extract_tweet_links(tweet)
    return response

generate_twitter_link_batch('guardian')
