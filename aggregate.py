import csv
import logging
import argparse
import datetime

import urllib2
import xml.etree.ElementTree as etree

import twitter

from parser import parse_content


def aggregate(mode='rss'):
    fetched_content = []
    if mode == 'rss':
        for category, urls in generate_rss_links():
            for url in fetch_links(urls):
                print "CHECK URL:\t"
                parsed_content = parse_content(url)
                if parsed_content['title'] != 'Log In' \
                        and parsed_content['lead_image_url']:
                    fetched_content.append(parsed_content)
                    print parsed_content['title']

    elif mode == 'twitter':
        print 'twitter mode'
    else:
        print 'error'


def generate_rss_links():
    with open('sources/rss.csv', 'rb') as f:
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        for line in csv_reader:
            category, link = line
            yield category.strip(), link.strip()


def fetch_links(urls):
    try:
        content = ''.join(urllib2.urlopen(urls))
        root = etree.fromstring(content)

        for i in parse_links(root):
            yield i

    except Exception as e:
        print "[EXCEPTION]:\t", e


def parse_links(node):
    itr = node.iter()
    try:
        for i in itr:
            if i.tag in ('item',):
                for j in i.getchildren():
                    if j.tag in ('link',):
                        yield j.text
    except StopIteration:
        pass


def logging_config():
    log_name = 'logs/aggregate_' + str(datetime.datetime.now()) + '.log'
    logging.basicConfig(filename=log_name, level=logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch content given \
      twitter username, domain combinations or rss list')
    parser.add_argument('-m', '--mode', help='rss for RSS feed, \
      twitter for Twitter feed')
    args = vars(parser.parse_args())

    aggregate(mode=args['mode'])
