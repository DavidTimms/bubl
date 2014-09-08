import webapp2
import logging
from google.appengine.api import users
import datastore
import view_renderer as view
from utils import check, urlify

class TopicHandler(webapp2.RequestHandler):
	def topic_page(self, topic_url):
		try:
			topic = check(
				self,
				datastore.Topic.retrieve(topic_url),
				'Sorry, we couldn\'t find that page.',
				404)
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

			self.response.write(view.render_topic_page(page_data))
		except AssertionError as e:
			logging.info(str(e.args))

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
			datastore.SearchIndexShard.add_topic(topic_url, topic_name)
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
			datastore.SearchIndexShard.remove_topic(topic_url, topic_name)
			#self.redirect(str(self.request.host_url))
			self.response.write('The page "' + topic_name + '" has been deleted.')
		except AssertionError as e:
			logging.info(str(e.args))
