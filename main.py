import webapp2
import logging
import re
from google.appengine.api import users
import datastore
import view_renderer as view
import imgur
from inspect import isfunction

def urlify(name):
	# split into list of words
	words = name.strip().lower().split(' ')
	# remove non-alphanumeric chars from each word
	words = map(lambda s: re.sub(r'\W', '', s), words)
	# remove empty strings
	words = [word for word in words if word]
	# join words with a dash
	return '-'.join(words)

def check(self, value, error_response):
	if value:
		return value
	else:
		if isfunction(error_response):
			error_response()
			raise AssertionError('Check failed')
		else:
			self.response.status = 400
			self.response.write(error_response)
			raise AssertionError('Check failed. ' + error_response)

class TopicHandler(webapp2.RequestHandler):
	def topic_page(self, topic_url):
		try:
			topic = check(
				self,
				datastore.Topic.retrieve(topic_url),
				'Topic not found')
			page_data = {
				'topic': topic.to_dict(),
				'images': topic.get_images()
			}

			user = users.get_current_user()
			if user:
				page_data['user'] = {
					'name': user.nickname(),
					'id': user.user_id()
				}

			#self.response.write(str(page_data))
			self.response.write(view.render_topic_page(page_data))
		except AssertionError as e:
			logging.info(str(e.args))
		#imgur.info('1FJzDyQ')

	def create_topic(self):
		try:
			user = check(
				self, 
				users.get_current_user(), 
				lambda: self.redirect(webapp2.uri_for('login')))
			topic_name = check(
				self,
				self.request.get('topic_name'),
				'Unable to create topic page. No topic name specified.')
			topic_url = urlify(self.request.get('topic_name'))
			while datastore.Topic.retrieve(topic_url) != None:
				topic_url += '!'
			datastore.Topic.create(topic_url, topic_name, user.user_id(), user.nickname())
			self.redirect(str(self.request.host_url + '/' + topic_url))
		except AssertionError as e:
			logging.info(str(e.args))
	def delete_topic(self):
		try:
			user = check(
				self, 
				users.get_current_user(), 
				lambda: self.redirect(webapp2.uri_for('login')))
			topic_url = check(
				self,
				self.request.get('topic_url'),
				'Unable to delete topic page. No topic specified.')
			topic = check(
				self,
				datastore.Topic.retrieve(topic_url),
				'Unable to delete topic page. Topic cannot be found.')
			correct_user = check(
				self,
				topic.creator_id == user.user_id(),
				'Unable to delete topic page. You are not the user who created the page.')
			topic_name = topic.name
			topic.key.delete()
			#self.redirect(str(self.request.host_url))
			self.response.write('The page "' + topic_name + '" has been deleted.')
		except AssertionError as e:
			logging.info(str(e.args))

class ImageHandler(webapp2.RequestHandler):
	def add_image(self, topic_url):
		user = users.get_current_user()
		image_caption = self.request.get('image_caption')
		if self.request.get('image_type') == 'file':
			res = imgur.upload({
				'image': self.request.get('image'),
				'title': image_caption
				})
			if res is None or res['success'] is False:
				self.response.write('Imgur upload failed')
				return
			logging.info(res['data'])
			image_url = res['data']['link']
			delete_hash = res['data']['deletehash']
		else:
			image_url = self.request.get('image_url')
		if (not user) or (not topic_url) or (not image_url) or (not image_caption):
			self.response.write('Image upload failed')
		else:
			datastore.Image.create(
				topic_url, 
				image_url, 
				image_caption,
				user.user_id(), 
				user.nickname(), 
				delete_hash)
			self.redirect(str(self.request.host_url + '/' + topic_url))
	def delete_image(self, topic_url):
		try:
			user = check(
				self, 
				users.get_current_user(), 
				'You are not logged in')
			user_id = user.user_id()
			image_id = check(
				self, 
				self.request.get('image_id'), 
				'No image ID specified')
			image = check(
				self, 
				datastore.Image.get_by_urlsafe_id(image_id), 
				'Image cannot be found')
			if image.creator_id != user.user_id():
				self.response.status = 401
				self.response.write('You are not the user who added that image')
			else:
				if image.delete_hash:
					imgur.delete(image.delete_hash)
					self.response.write('image deleted from imgur\n')
				image.delete()
				self.response.write('image deleted from bubl')
		except AssertionError as e:
			logging.info(str(e.args))
	def vote(self):
		try:
			user = check(
				self, 
				users.get_current_user(), 
				'You are not logged in')
			user_id = user.user_id()
			image_id = check(
				self, 
				self.request.get('image_id'), 
				'No image ID specified')
			image = check(
				self, 
				datastore.Image.get_by_urlsafe_id(image_id), 
				'Image cannot be found')
			vote_type = self.request.get('vote_type')
			check(
				self, 
				vote_type == 'up' or vote_type == 'down', 
				'Invalid vote type')
			if vote_type == 'up':
				if user_id in image.upvoters:
					image.upvoters.remove(user_id)
					self.response.write('upvote removed')
				else:
					image.upvoters.append(user_id)
					self.response.write('upvote added')
					if user_id in image.downvoters:
						image.downvoters.remove(user_id)
			if vote_type == 'down':
				if user_id in image.downvoters:
					image.downvoters.remove(user_id)
					self.response.write('downvote removed')
				else:
					image.downvoters.append(user_id)
					self.response.write('downvote added')
					if user_id in image.upvoters:
						image.upvoters.remove(user_id)
			image.recalc_score()
			image.put()
		except AssertionError as e:
			logging.info(str(e.args))

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

app = webapp2.WSGIApplication([
	webapp2.Route('/login', 
		handler=UserHandler, 
		name='login', 
		handler_method='login'),
	webapp2.Route('/logout', 
		handler=UserHandler, 
		name='logout', 
		handler_method='logout'),
	webapp2.Route('/create_topic', 
		handler=TopicHandler, 
		name='create-topic', 
		handler_method='create_topic'),
	webapp2.Route('/delete_topic', 
		handler=TopicHandler, 
		name='delete-topic', 
		handler_method='delete_topic'),
	webapp2.Route('/<topic_url>/add_image', 
		handler=ImageHandler, 
		name='add-image', 
		handler_method='add_image'),
	webapp2.Route('/<topic_url>/delete_image', 
		handler=ImageHandler, 
		name='delete-image', 
		handler_method='delete_image'),
	webapp2.Route('/vote', 
		handler=ImageHandler, 
		name='vote', 
		handler_method='vote'),
	webapp2.Route('/<topic_url>', 
		handler=TopicHandler, 
		name='topic-page',
		handler_method='topic_page')
], debug=True)
