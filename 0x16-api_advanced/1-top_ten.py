#!/usr/bin/python3
'''prints the titles of the first 10 hot posts listed for a given subreddit'''
import requests


def top_ten(subreddit):
    ''' get top 10 titles'''

    url = 'http://reddit.com/r/{}/hot.json'
    headers = {'User-agent': 'colombiandreamm'}
    payload = {'limit': '10'}
    response = requests.get(url.format(subreddit),
                            headers=headers, params=payload)
    if response.status_code == 200:
        top10 = response.json()
        for i in range(10):
            print(top10['data']['children'][i]['data']['title'])
    else:
        return print("None")
