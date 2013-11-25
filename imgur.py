import logging
import json
import urllib
from google.appengine.api import urlfetch

api_url = 'https://api.imgur.com/3/'
client_id =  '22a551b53de42cc'
client_secret = '392a1344ed9c8b040f6439e5cb8a0208cf4169b5'

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
			return res
	except urlfetch.Error as e:
		logging.error('Imgur error: invalid request')

def upload(data):
	endpoint = 'upload'
	data['type'] = 'file'
	enc_data = urllib.urlencode(data)
	res = send_request(endpoint, data=enc_data)
	return json.loads(res.content)

def info(imgur_id):
	endpoint = 'image/' + imgur_id
	res = send_request(endpoint, method=urlfetch.GET)
	return json.loads(res.content)