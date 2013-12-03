import webapp2
import logging
from handlers.home import HomeHandler
from handlers.topic import TopicHandler
from handlers.image import ImageHandler
from handlers.user import UserHandler

app = webapp2.WSGIApplication([
	webapp2.Route('/', 
		handler=HomeHandler, 
		name='homepage', 
		handler_method='homepage'),
	webapp2.Route('/search', 
		handler=HomeHandler, 
		name='search', 
		handler_method='search'),
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
