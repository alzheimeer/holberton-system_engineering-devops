#!/usr/bin/python3
'''returns a list containing the titles of all hot articles for a given subreddit'''
import requests


def recurse(subreddit, hot_list=[], after=""):
    ''' recursive function'''

    url = 'http://reddit.com/r/{}/hot.json?after={}'
    headers = {'User-agent': 'colombiandreamm'}
    response = requests.get(url.format(subreddit, after),
                            headers=headers)
    if response.status_code == 200:
        key = response['data']['after']
        parent = response['data']['children']
        for obj in parent:
            hot_list.append(obj['data']['title'])
        if key is not None:
            recurse(subreddit, hot_list, key)
        return hot_list

    #    top10 = response.json()
    #    for i in range(10):
    #        print(top10['data']['children'][i]['data']['title'])
    else:
        return print("None")