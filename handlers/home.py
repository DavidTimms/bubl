import webapp2
import logging
from google.appengine.api import users
import view_renderer as view

class HomeHandler(webapp2.RequestHandler):
	def homepage(self):
		user = users.get_current_user()
		page_data = dict()
		if user:
			page_data['user'] = {
				'name': user.nickname(),
				'id': user.user_id()
			}

		#self.response.write(str(page_data))
		self.response.write(view.render('home-page', page_data))