import csv
import urllib2
import xml.etree.ElementTree as etree


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