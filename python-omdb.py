#!/usr/bin/env python3

import json
import os
import sys
import urllib.request

# Get a new one at http://www.omdbapi.com/apikey.aspx
API_KEY = 'a1078617'

# Name of the script for putting in error messages, probably just python-omdb.py
NAME = os.path.basename(sys.argv[0])

title = input('title > ')

# Error handling is for pussies!
# (error handling is not actually for pussies, fix this)
response = json.loads(urllib.request.urlopen(f'http://www.omdbapi.com/?apikey={API_KEY}&t={urllib.parse.quote_plus(title)}').read().decode('utf-8'))

if response["Response"] == "False":
    print(f'{NAME}: error: {response["Error"]}', file=sys.stderr)
    sys.exit(1)

# There's some quote from Staples that comes to mind, I just can't think what it is...
print(f'Title: {response["Title"]}')
print(f'Year: {response["Year"]}')
print(f'Actors: {response["Actors"].split(", ")}')
print(f'Plot: {response["Plot"]}')
