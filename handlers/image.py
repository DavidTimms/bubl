import webapp2
import logging
from google.appengine.api import users
import datastore
import imgur
from inspect import isfunction

def check(self, value, error_response, status=400):
	if value:
		return value
	else:
		if isfunction(error_response):
			error_response()
			raise AssertionError('Check failed')
		else:
			self.response.status = status
			self.response.write(error_response)
			raise AssertionError('Check failed. ' + error_response)

class ImageHandler(webapp2.RequestHandler):
	def add_image(self, topic_url):
		user = users.get_current_user()
		image_caption = self.request.get('image_caption')
		delete_hash = None
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
