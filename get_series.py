import os
import sys
from urllib2 import urlopen
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(r'config.txt'))

apikey = config.get('Sonarr Config', 'apikey')
host = config.get('Sonarr Config', 'host')
port = config.get('Sonarr Config', 'port')

url = 'http://'+host+':'+port+'/api/series?apikey='+apikey

response = urlopen(url)
shows = json.loads(response.read())
shownames = []

for show in shows:
    # now song is a dictionary  
	shownames.append(show['title'])

found = shownames

for f in found:
	print f