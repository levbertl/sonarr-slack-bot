import os
import sys
from urllib2 import urlopen
import urllib
import json
import ConfigParser



def escape(str):
	out = str.replace('&', '&amp;')
	out = out.replace('<', '&lt;')
	out = out.replace('>', '&gt;')
	return out

def search_show(show, prefix):
	config = ConfigParser.ConfigParser()
	config.readfp(open(r'config.txt'))
	apikey = config.get('Sonarr Config', 'apikey')
	host = config.get('Sonarr Config', 'host')
	port = config.get('Sonarr Config', 'port')
	url = 'http://'+host+':'+port+'/api/series?apikey='+apikey
	url = url+'&term='
	term = show.replace(prefix,'')
	url += term.replace(' ','%20')
	response = urlopen(url)
	shows = json.loads(response.read())
	out = {}

	attachments = []

	for show in shows:
	    	item = {}
	    	item['fallback'] = escape(show['title'])
	    	item['pretext'] = 'movie'
	    	item['color'] = '#36a64f'
	    	if('network' in show):
	    		item['author_name'] = escape(show['network'])
	    	item['title'] = escape(show['title'])
	    	if('imdbId' in show):
	    		imdb = 'http://www.imdb.com/title/' + show['imdbId']
	    		item['title_link'] = escape(imdb)
    		if('overview' in show):
	    		item['text'] = escape(show['overview'])
	    	
	    	
	    	if('status' in show):
	    		item['fields'] = []
	    		fields = {}
	    		fields['title'] = show['status']
	    		item['fields'].append(fields)
	    	if('remotePoster' in show):
	    		item['image_url'] = escape(show['remotePoster'])
		attachments.append(item)
	out['attachments'] = attachments
	out['unfurl_media'] = True
	out['unfurl_links'] = True
	out['text'] = "test"
	o = []
	o.append(out)

	return json.dumps(attachments)


