import urllib2
import json
from credentials import readability_api_token


def parse_content(url, version='v1'):
    '''
    Parse URL to extract relevent content information

    Reference:
        https://www.readability.com/developers/api/parser

    Returns:
        {
            'domain',
            'title',
            'date_published',
            'author',
            'excerpt',
            'content',
            'word_count',
            'lead_image_url',
            'url'
        }
    '''
    url = url.replace("#", "%23")
    endpoint = 'http://readability.com/api/content/' \
        + version + '/parser?url=' \
        + url + '&token=' + readability_api_token
    try:
        req = urllib2.urlopen(endpoint)
        res = json.loads(req.read())
    except Exception:
        print "[EXCEPTION]:\tParser Error"
        res = None
    return res
