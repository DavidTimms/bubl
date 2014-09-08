from google.appengine.ext import ndb
import logging
import random

class Topic(ndb.Model):
	url = ndb.StringProperty()
	name = ndb.StringProperty()
	creator_id = ndb.StringProperty()
	creator_name = ndb.StringProperty()

	def get_images(self):
		return map(lambda x: x.to_dict(), Image.topic_images(self.url))

	@classmethod
	def create(cls, topic_url, topic_name, creator_id, creator_name):
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
		anc_key = ndb.Key("Topic", topic_url)
		return cls.query(ancestor = anc_key).order(-cls.score).fetch(30)

SEARCH_SHARD_COUNT = 12

class SearchIndexShard(ndb.Model):
	index = ndb.PickleProperty(default = list())

	@classmethod
	def build_index(cls):
		index = list()
		for shard in cls.query():
			index.extend(shard.index)
		return index

	@classmethod
	@ndb.transactional
	def add_topic(cls, topic_url, topic_name):
		shard_num = str(random.randint(0, SEARCH_SHARD_COUNT - 1))
		# logging.info('adding ' + topic_name + ' to shard ' + str(shard_num))
		shard = cls.get_by_id(shard_num)
		if shard is None:
			logging.info('creating shard')
			shard = cls(id=shard_num)
		shard.index.append((topic_url, topic_name))
		# logging.info('shard contents: ' + str(shard.index))
		shard.put()

	@classmethod
	def remove_topic(cls, topic_url, topic_name):
		topic = (topic_url, topic_name)
		for shard_num in range(0, SEARCH_SHARD_COUNT):
			shard = cls.get_by_id(str(shard_num))
			if shard is not None and topic in shard.index:
				shard.index.remove(topic)
				shard.put()