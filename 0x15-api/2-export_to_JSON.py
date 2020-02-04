#!/usr/bin/python3
"""export data in the JSON format."""

import json
import requests
import sys

if __name__ == "__main__":
    url = 'https://jsonplaceholder.typicode.com/'
    params = (('userId', sys.argv[1]),)
    response0 = requests.get(url + 'todos/', params=params)
    if response0.status_code == 200:
        t = response0.json()

    params = (('id', sys.argv[1]),)
    response1 = requests.get(url + 'users/', params=params)
    if response1.status_code == 200:
        user = response1.json()

    ll = []
    for task in t:
        td = {}
        td["task"] = task['title']
        td["completed"] = task['completed']
        td["username"] = user[0]['username']
        ll.append(td)
    jsonX = {}
    jsonX[sys.argv[1]] = ll
    with open("{}.json".format(sys.argv[1]), 'w') as jsonfile:
        json.dump(jsonX, jsonfile)
