#!/usr/bin/python3
"""export data in the CSV format"""

import csv
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

    with open("{}.csv".format(sys.argv[1]), 'w', newline='') as csvfile:
        cvsW = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for task in t:
            cvsW.writerow([int(sys.argv[1]), user[0]['username'],
                           task['completed'], task['title']])
