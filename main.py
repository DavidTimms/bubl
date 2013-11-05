import webapp2
import jinja2
import os
import logging
from google.appengine.api import users
import datastore

# Initialise jinja2 templating environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
def render(template_url, data):
		template = JINJA_ENVIRONMENT.get_template(template_url)
		return template.render(data)

class TopicHandler(webapp2.RequestHandler):
	def topic_page(self, topic_url):
		topic = datastore.Topic.retrieve(topic_url)
		if topic == None:
			self.response.write('Topic not found')
		else:
			page_data = topic.to_dict()
			user = users.get_current_user()
			if user:
				page_data['logged_in'] = True
				page_data['user_name'] = user.nickname()
				page_data['user_id'] = user.user_id()
			self.response.write(render('page.html', page_data))

	def create_topic(self, topic_url):
		user = users.get_current_user()
		topic_url = self.request.get('topic_url')
		topic_name = self.request.get('topic_name')
		if (not user) or (not topic_name) or (not topic_name):
			self.response.write('Page creation failed')
		else:
			datastore.Topic.create(topic_url, topic_name, user.user_id(), user.nickname())
			self.redirect(str(self.request.host_url + '/' + topic_url))
	def delete_topic(self, topic_url):
		res = 'Topic page deleted (not really): ' + topic_url
		self.response.write(res)

class ImageHandler(webapp2.RequestHandler):
	def add_image(self, topic_url):
		user = users.get_current_user()
		image_url = self.request.get('image_url')
		image_caption = self.request.get('image_caption')
		if (not user) or (not topic_url) or (not image_url) or (not image_caption):
			self.response.write('Image upload failed')
		else:
			datastore.Image.create(topic_url, image_url, image_caption, user.user_id(), user.nickname())
			self.redirect(str(self.request.host_url + '/' + topic_url))

class UserHandler(webapp2.RequestHandler):
	def login(self):
		return_url = self.request.host_url + '/' + self.request.GET['topic_url']
		self.redirect(users.create_login_url(return_url))
	def logout(self):
		return_url = self.request.host_url + '/' + self.request.GET['topic_url']
		self.redirect(users.create_logout_url(return_url))

app = webapp2.WSGIApplication([
	webapp2.Route('/login', 
		handler=UserHandler, 
		name='login', 
		handler_method='login'),
	webapp2.Route('/logout', 
		handler=UserHandler, 
		name='logout', 
		handler_method='logout'),
	webapp2.Route('/<topic_url>/create', 
		handler=TopicHandler, 
		name='create-topic', 
		handler_method='create_topic'),
	webapp2.Route('/<topic_url>/delete', 
		handler=TopicHandler, 
		name='delete-topic', 
		handler_method='delete_topic'),
	webapp2.Route('/<topic_url>/add_image', 
		handler=ImageHandler, 
		name='add-image', 
		handler_method='add_image'),
	webapp2.Route('/<topic_url>', 
		handler=TopicHandler, 
		name='topic-page',
		handler_method='topic_page')
], debug=True)
