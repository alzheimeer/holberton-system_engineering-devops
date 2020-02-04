#!/usr/bin/python3
"""export data in the JSON format."""

import json
import requests
import sys

if __name__ == "__main__":
    url = 'https://jsonplaceholder.typicode.com/todos'
    params = (('userId', sys.argv[1]),)
    response0 = requests.get(url, params=params)
    if response0.status_code == 200:
        t = response0.json()

    url = 'https://jsonplaceholder.typicode.com/users'
    params = (('id', sys.argv[1]),)
    response1 = requests.get(url, params=params)
    if response1.status_code == 200:
        user = response1.json()
    tasks = []
    for task in t:
        task_dict = {}
        task_dict["task"] = task['title']
        task_dict["completed"] = task['completed']
        task_dict["username"] = user[0]['username']
        tasks.append(task_dict)
    jsonX = {}
    jsonX[sys.argv[1]] = tasks
    with open("{}.json".format(sys.argv[1]), 'w') as jsonfile:
        json.dump(jsonX, jsonfile)
