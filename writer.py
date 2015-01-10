import datetime


def write_to_db(client, raw_content):
    # create the content object
    content = {}
    content['domain'] = raw_content['domain']
    content['url'] = raw_content['url']
    content['title'] = raw_content['title']
    content['date_published'] = raw_content['date_published']
    content['author'] = raw_content['author']
    content['excerpt'] = raw_content['excerpt']
    content['content'] = raw_content['content']
    content['lead_image_url'] = raw_content['lead_image_url']
    content['word_count'] = raw_content['word_count']

    content['view_count'] = 0
    content['share_count'] = 0

    content['nodes'] = []
    content['discussions'] = []

    content['category'] = None

    # Check to ensure this link is not inserted already
    if client['content_db']['content_collection'].find_one({'url': content['url']}):
        return False

    content['_id'] = client['content_db']['content_collection'].insert(content)

    # create the associated public discussion object
    discussion = {}
    discussion['content'] = [content['_id']]
    discussion['scope'] = 'public'
    discussion['participants'] = []
    discussion['messages'] = []
    discussion['date_modified'] = datetime.datetime.now()
    discussion['date_created'] = datetime.datetime.now()

    discussion['_id'] = client['discussion_db']['discussion_collection'].insert(discussion)

    # Associated the discussion object to the Content object
    content['discussions'] = [discussion['_id']]
    client['discussion_db']['discussion_collection'].update(
        {'_id': content['_id']},{'$set': content}, upsert=False)
