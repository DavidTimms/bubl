import webapp2
import logging
from google.appengine.api import users

class UserHandler(webapp2.RequestHandler):
	def login(self):
		return_url = self.request.host_url + '/'
		if 'topic_url' in self.request.GET:
			return_url += self.request.GET['topic_url']
		self.redirect(users.create_login_url(return_url))
	def logout(self):
		return_url = self.request.host_url + '/'
		if 'topic_url' in self.request.GET:
			return_url += self.request.GET['topic_url']
		self.redirect(users.create_logout_url(return_url))
