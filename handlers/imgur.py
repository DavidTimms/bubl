import logging
import json
import urllib
from google.appengine.api import urlfetch
from imgur_details import client_id, client_secret

api_url = 'https://api.imgur.com/3/'

def send_request(endpoint, method=urlfetch.POST, data=None):
	endpoint = api_url + endpoint + '.json'
	try:
		res = urlfetch.fetch(
			url = endpoint,
			method = method,
			payload = data,
			headers = {'Authorization': 'Client-ID ' + client_id})
		if res.status_code != 200:
			logging.error('Imgur Error: status code = ' + str(res.status_code))
		else:
			return json.loads(res.content)
	except urlfetch.Error as e:
		logging.error('Imgur error: invalid request')

def upload(data):
	endpoint = 'upload'
	data['type'] = 'file'
	enc_data = urllib.urlencode(data)
	return send_request(endpoint, data=enc_data)

def info(imgur_id):
	endpoint = 'image/' + imgur_id
	return send_request(endpoint, method=urlfetch.GET)

def delete(delete_hash):
	endpoint = 'image/' + delete_hash
	return send_request(endpoint, method=urlfetch.DELETE)