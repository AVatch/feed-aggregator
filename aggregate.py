import argparse
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
                        print parsed_content['domain'], '\t', \
                            parsed_content['title']

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
                        print parsed_content['domain'], '\t', \
                            parsed_content['title']
    else:
        print 'error'


if __name__ == '__main__':
    # Setup the arguments
    parser = argparse.ArgumentParser(description='Fetch content given \
      twitter username, domain combinations or rss list')
    parser.add_argument('-m', '--mode', help='rss for RSS feed, \
      twitter for Twitter feed')
    parser.add_argument('-w', '--write', help='0 for stream, \
        1 for write to mongo')
    args = vars(parser.parse_args())

    # Call main function
    aggregate(mode=args['mode'], write=int(args['write']))
