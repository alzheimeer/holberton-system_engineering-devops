#!/usr/bin/python3
"""export data in the JSON format. diferent conditions"""

import json
import requests
import sys

if __name__ == "__main__":
    url = 'https://jsonplaceholder.typicode.com/'
    response0 = requests.get(url + 'todos/')
    if response0.status_code == 200:
        t = response0.json()

    response1 = requests.get(url + 'users/')
    if response1.status_code == 200:
        users = response1.json()

    dicx = {}
    for user in users:
        username = user['username']
        ll = []
        for task in t:
            if task['userId'] == user['id']:
                di = {}
                di['username'] = username
                di['task'] = task['title']
                di['completed'] = task['completed']
                ll.append(di)
        dicx[user['id']] = ll

    with open("todo_all_employees.json", 'w') as f:
        json.dump(dicx, f)
