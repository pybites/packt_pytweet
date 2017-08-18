from collections import namedtuple
import os
import socket
import sys

from bs4 import BeautifulSoup as Soup
import requests

from config import logging, api

BASE_URL = 'https://www.packtpub.com'
FREE_LEARNING_PAGE = 'free-learning'
PACKT_FREE_LEARNING_LINK = BASE_URL + '/packt/offers/' + FREE_LEARNING_PAGE

FILTERS = 'Python Django Flask'.split()
TWEET = 'Free @PacktPub ebook of the day: {} - {}'
HEADERS = {'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '  # noqa E501
           '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

Book = namedtuple('Book', 'title description summary image link')


def retrieve_page_html():
    if os.path.isfile(FREE_LEARNING_PAGE):
        with open(FREE_LEARNING_PAGE) as f:
            return f.read()
    else:
        return requests.get(PACKT_FREE_LEARNING_LINK, headers=HEADERS).text


def extract_book_data_page(content):
    soup = Soup(content, 'html.parser')
    book_image = soup.find('div', {'class': 'dotd-main-book-image'})
    link = BASE_URL + book_image.find('a').get('href')
    image = 'https:' + book_image.find('img').get('src')
    book_main = soup.find('div', {'class': 'dotd-main-book-summary'})
    title_div = book_main.find('div', {'class': 'dotd-title'})
    title = title_div.find('h2').text.strip()
    descr_div = title_div.find_next_sibling("div")
    description = descr_div.text.strip()
    summary_html = descr_div.find_next_sibling("div")
    # sometimes 2nd paragraph = form, then don't include it
    if 'dotd-main-book-form' in str(summary_html):
        summary_html = ''
    return Book(title=title,
                description=description,
                summary=summary_html,
                image=image,
                link=link)


def tweet_status(tweet):
    try:
        api.update_status(tweet)
        logging.info('Posted to Twitter')
    except Exception as exc:
        logging.error('Error posting to Twitter: {}'.format(exc))


def title_match(title, filters=FILTERS):
    title = title.lower()
    return any(term.lower() in title for term in filters)


def hashify(tweet, filters=FILTERS):
    for term in filters:
        tweet = tweet.replace(term, '#' + term)
    return tweet


if __name__ == '__main__':
    local = 'MacBook' in socket.gethostname()
    test = local or 'dry' in sys.argv[1:]

    content = retrieve_page_html()
    book = extract_book_data_page(content)

    if not title_match(book.title):
        logging.info('filter: {} not in title: {}'.format(str(FILTERS),
                                                          book.title))
        sys.exit(1)

    tweet = TWEET.format(book.title, PACKT_FREE_LEARNING_LINK)
    tweet = hashify(tweet)

    if test:
        logging.info('Test: tweet to send: {}'.format(tweet))
    else:
        tweet_status(tweet)
