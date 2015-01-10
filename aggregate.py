import logging
import argparse
import datetime
import pymongo

from rss_helpers import *
from twitter_helpers import *
from writer import *
from parser import parse_content


def aggregate(mode='rss', write=False):
    fetched_content = []
    if write:
        client = pymongo.MongoClient('localhost', 27017)

    if mode == 'rss':
        for category, urls in generate_rss_links():
            print "*"*50
            print category
            for url in fetch_links(urls):
                parsed_content = parse_content(url)
                if parsed_content:
                    if parsed_content['title'] != 'Log In' \
                            and parsed_content['lead_image_url']:
                        fetched_content.append(parsed_content)
                        if write:
                            write_to_db(client, parsed_content)
                        print parsed_content['domain'], '\t', parsed_content['title']

    elif mode == 'twitter':
        api = generate_twitter_api()
        for username, domain in parse_twitter_usernames():
            for url in generate_twitter_urls(api, username):
                parsed_content = parse_content(url)
                if parsed_content:
                    if parsed_content['lead_image_url'] \
                            and parsed_content['domain'] == domain:
                        fetched_content.append(parsed_content)
                        if write:
                            write_to_db(client, parsed_content)
                        print parsed_content['domain'], '\t', parsed_content['title']
    else:
        print 'error'


def logging_config():
    log_name = 'logs/aggregate_' + str(datetime.datetime.now()) + '.log'
    logging.basicConfig(filename=log_name, level=logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch content given \
      twitter username, domain combinations or rss list')
    parser.add_argument('-m', '--mode', help='rss for RSS feed, \
      twitter for Twitter feed')
    args = vars(parser.parse_args())

    aggregate(mode=args['mode'], write=True)
