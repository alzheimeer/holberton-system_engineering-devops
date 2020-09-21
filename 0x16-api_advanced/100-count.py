#!/usr/bin/python3
'''that queries the Reddit API and returns the number of subscribers'''
import re
import requests
import sys


def count_words(subreddit, word_list, after="", to_print={}):
    """
    Queries the Reddit API
    """

    if after == "":
        for word in word_list:
            to_print[word] = 0

    url = "https://www.reddit.com/r/{}/hot.json{}".format(subreddit, after)

    json_obj = requests.get(url, headers={'User-Agent': 'My User Agent 1.0'})

    if json_obj.status_code != 404:
        dict_obj = json_obj.json()
        list_obj = dict_obj.get('data').get('children')

    for each in list_obj:
        title = each.get('data').get('title')
        tit_list = title.split()
        for word in word_list:
            c = re.compile(r"^{}$".format(word), re.I)
            for each_tit_w in tit_list:
                res = c.findall(each_tit_w)
                to_print[word] += len(res)

    next_fullname = dict_obj.get('data').get('after')
    after = "?after={}".format(next_fullname)

    if next_fullname is not None:
        count_words(subreddit, word_list, after, to_print)
    else:
        sorted_l = sorted(to_print.items(), key=lambda x: x[1])
        sorted_l.reverse()

        for x in sorted_l:
            if x[1] != 0:
                print("{}: {}".format(x[0], x[1]))

    return None