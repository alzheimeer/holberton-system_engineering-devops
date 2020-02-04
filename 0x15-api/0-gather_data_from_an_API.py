#!/usr/bin/python3
'''get employeed information with ID'''
import requests
import json
import sys


if __name__ == "__main__":
    url = 'https://jsonplaceholder.typicode.com/'
    args = {'userId': sys.argv[1]}
    args1 = {'id': sys.argv[1]}
    # Get todo list
    response0 = requests.get(url + 'todos/', params=args)
    # Get user info
    response1 = requests.get(url + 'users/', params=args1)
    if response0.status_code == 200:
        user = response0.json()
        a = 0
        b = 0
        c = []
        for n in user:
            if (n.get('completed')) is True:
                a = a+1
                c.append(n.get('title'))
            b = b+1
    if response1.status_code == 200:
        t = response1.json()
        print("Employee {} is done with tasks({}/{}):"
              .format(t[0]['name'], a, b))
        if len(c) > 0:
            for list in c:
                print("\t {}".format(list))
