from google.appengine.ext import ndb
import logging

class Topic(ndb.Model):
	url = ndb.StringProperty()
	name = ndb.StringProperty()
	creator_id = ndb.StringProperty()
	creator_name = ndb.StringProperty()

	def get_images(self):
		return map(lambda x: x.to_dict(), Image.topic_images(self.url))
	#@staticmethod
	#def ancestor():
	#	return ndb.Key("TopicSet", "master")
	@classmethod
	def create(cls, topic_url, topic_name, creator_id, creator_name):
		#topic = Topic(
		#	parent = cls.ancestor(),
		#	url = topic_url,
		#	name = topic_name,
		#	creator_name = creator_name,
		#	creator_id = creator_id)
		topic = cls.get_or_insert(topic_url)
		if topic.url == topic_url:
			raise Exception('topic URL already in use')
		topic.url = topic_url
		topic.name = topic_name
		topic.creator_name = creator_name
		topic.creator_id = creator_id
		topic.put()
		return topic

	@classmethod
	def retrieve(cls, url):
		return ndb.Key("Topic", url).get()
		#return cls.query(Topic.url == url, ancestor = cls.ancestor()).get()

class Image(ndb.Model):
	url = ndb.StringProperty()
	caption = ndb.StringProperty()
	creator_id = ndb.StringProperty()
	creator_name = ndb.StringProperty()
	upvoters = ndb.PickleProperty()
	downvoters = ndb.PickleProperty()
	score = ndb.IntegerProperty()
	delete_hash = ndb.StringProperty()

	def recalc_score(self):
		self.score = len(self.upvoters) - len(self.downvoters)
		return self.score

	def to_dict(self):
		d = super(Image, self).to_dict()
		d['key'] = self.key.urlsafe()
		if ('imgur.com' in self.url):
			# set the imgur medium sized image url as thumbnail
			parts = self.url.split('.')
			d['thumb_url'] = '.'.join(parts[:-1]) + 'm.' + parts[-1]
		else:
			d['thumb_url'] = self.url
		return d

	def delete(self):
		self.key.delete()

	@classmethod
	def get_by_urlsafe_id(cls, urlsafe_id):
		return ndb.Key(urlsafe = urlsafe_id).get()

	@classmethod
	def create(cls, topic_url, image_url, image_caption, creator_id, creator_name, delete_hash):
		image = Image(
			parent = Topic.retrieve(topic_url).key,
			url = image_url,
			caption = image_caption,
			creator_name = creator_name,
			creator_id = creator_id,
			upvoters = list(),
			downvoters = list(),
			score = 0,
			delete_hash = delete_hash)
		return image.put()

	@classmethod
	def topic_images(cls, topic_url):
		anc_key = Topic.retrieve(topic_url).key
		return cls.query(ancestor = anc_key).order(-cls.score).fetch(30)