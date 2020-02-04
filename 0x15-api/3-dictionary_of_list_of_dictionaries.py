#!/usr/bin/python3
"""export data in the JSON format. diferent conditions"""

import json
import requests
import sys

if __name__ == "__main__":
    url = 'https://jsonplaceholder.typicode.com/todos'
    response0 = requests.get(url)
    if response0.status_code == 200:
        t = response0.json()

    url = 'https://jsonplaceholder.typicode.com/users'
    response1 = requests.get(url)
    if response1.status_code == 200:
        users = response1.json()

    dicx = {}
    for user in users:
        username = user['username']
        pepe = []
        for task in t:
            if task['userId'] == user['id']:
                dict_info = {}
                dict_info['username'] = username
                dict_info['task'] = task['title']
                dict_info['completed'] = task['completed']
                pepe.append(dict_info)
        dicx[user['id']] = pepe

    with open("todo_all_employees.json", 'w') as f:
        json.dump(dicx, f)
