#!/usr/bin/python3
'''that queries the Reddit API and returns the number of subscribers'''
import requests


def count_words(subreddit, word_list):
    """Returns the count of given words"""
    try:
        url = 'https://www.reddit.com/r/' + subreddit + '/hot.json'
        header = {'User-agent': 'colombiandreamm'}
        limit = {'limit': '10'}
        resp = requests.get(url, headers=header,
                            params=limit, allow_redirects=False).json()
        key = resp.get('data').get('children')
        for value in key:
            print(value.get('data').get('title'))
    except:
        print(None)