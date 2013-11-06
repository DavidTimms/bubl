from google.appengine.ext import ndb
import logging

class Topic(ndb.Model):
	url = ndb.StringProperty()
	name = ndb.StringProperty()
	creator_id = ndb.StringProperty()
	creator_name = ndb.StringProperty()

	def to_dict(self):
		props = ['url', 'name', 'creator_id', 'creator_name']
		return dict(map(lambda x: (x, getattr(self, x)), props))

	def get_images(self):
		return map(lambda x: x.to_dict(), Image.topic_images(self.url))
	@staticmethod
	def ancestor():
		return ndb.Key("TopicSet", "master")
	@classmethod
	def create(cls, topic_url, topic_name, creator_id, creator_name):
		topic = Topic(
			parent = cls.ancestor(),
			url = str(topic_url),
			name = topic_name,
			creator_name = creator_name,
			creator_id = creator_id)
		return topic.put()

	@classmethod
	def retrieve(cls, url):
		return cls.query(Topic.url == url).get()

class Image(ndb.Model):
	url = ndb.StringProperty()
	caption = ndb.StringProperty()
	creator_id = ndb.StringProperty()
	creator_name = ndb.StringProperty()
	upvoters = ndb.PickleProperty()
	downvoters = ndb.PickleProperty()

	def to_dict(self):
		props = ['url', 'caption', 'creator_id', 'creator_name', 'upvoters', 'downvoters']
		return dict(map(lambda x: (x, getattr(self, x)), props))

	@classmethod
	def create(cls, topic_url, image_url, image_caption, creator_id, creator_name):
		image = Image(
			parent = Topic.retrieve(topic_url).key,
			url = image_url,
			caption = image_caption,
			creator_name = creator_name,
			creator_id = creator_id,
			upvoters = list(),
			downvoters = list())
		return image.put()

	@classmethod
	def topic_images(cls, topic_url):
		anc_key = Topic.retrieve(topic_url).key
		return cls.query(ancestor = anc_key).fetch(30)