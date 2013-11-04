#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import logging
from google.appengine.api import users

# Initialise jinja2 templating environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class TopicPageHandler(webapp2.RequestHandler):
	def get(self, topic_url):
		page_data = {
			'topic_name': topic_url,
			'topic_url': topic_url,
			'images': ['Photo One', 'Image Two', 'Picture Three']
		}

		user = users.get_current_user()
		if user:
			page_data['username'] = user.nickname()

		template = JINJA_ENVIRONMENT.get_template('page.html')
		self.response.write(template.render(page_data))
	def post(self, topic_url):
		res = 'Topic page created: ' + self.request.POST['topic_name']
		self.response.write(res)

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		return_url = self.request.host_url + '/' + self.request.GET['topic_url']
		self.redirect(users.create_login_url(return_url))

app = webapp2.WSGIApplication([
	webapp2.Route('/login', handler=LoginHandler, name='login-redirect'),
	webapp2.Route('/<topic_url>', handler=TopicPageHandler, name='topic-page')
], debug=True)
