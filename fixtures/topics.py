
import os
import random
import loremipsum
from zerqu.models import Topic, TopicLike, Comment

DATADIR = os.path.join(os.path.dirname(__file__), 'data')
markdown_contents = []
for name in os.listdir(DATADIR):
    if name.endswith('.md'):
        with open(os.path.join(DATADIR, name), 'rb') as f:
            content = f.read()
            markdown_contents.append(content.encode('utf-8'))


TYPEWRITER = (
    'https://d262ilb51hltx0.cloudfront.net/max/1600/'
    '1*TI7VtPCCe6bPi9xc-k_W1w.jpeg'
)


def create_topic(i, cafe_id, user_id):
    title = loremipsum.generate_sentence()[2]
    paragraphs = loremipsum.generate_paragraphs(random.randint(3, 7))
    paragraphs = [p[2] for p in paragraphs]
    md_content = random.choice(markdown_contents)
    index = random.randint(0, len(paragraphs))
    paragraphs.insert(index, md_content)
    content = '\n\n'.join(paragraphs)
    return {
        "id": i,
        "title": title,
        "content": content,
        "cafe_id": cafe_id,
        "user_id": user_id,
    }


def iter_user_topics():
    print('Creating topics')
    for i in range(1, 500):
        yield create_topic(i, random.randint(1, 16), random.randint(1, 500))
    for i in range(500, 620):
        yield create_topic(i, random.randint(1, 3), random.randint(1, 3))


def iter_topic_likes():
    print('Creating topics likes')
    for i in range(1, 2000):
        yield {
            "topic_id": random.randint(1, 62),
            "user_id": random.randint(2, 1000),
        }


def iter_comments():
    print('Creating comments')

    def sub(text):
        count = random.randint(10, 200)
        return text[:count]

    for i in range(1, 2400):
        paragraphs = loremipsum.generate_paragraphs(random.randint(1, 3))
        content = '\n\n'.join(sub(p[2]) for p in paragraphs)
        yield {
            "id": i,
            "topic_id": random.randint(400, 600),
            "user_id": random.randint(2, 1000),
            "content": content[:400]
        }


def iter_data():
    for data in iter_user_topics():
        if data['id'] == 1:
            data['cafe_id'] = 1
            data['info'] = {'cover': TYPEWRITER}
        yield Topic(**data)

    for data in iter_topic_likes():
        yield TopicLike(**data)

    for data in iter_comments():
        yield Comment(**data)
