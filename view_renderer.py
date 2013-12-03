import jinja2
import logging
import os

# Initialise jinja2 templating environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def render(template_url, data):
		template_url = 'templates/' + template_url + '.html'
		template = JINJA_ENVIRONMENT.get_template(template_url)
		return template.render(data)

def render_topic_page(data):
	def thumb_url(url, modifier):
		if ('imgur.com' in url):
			parts = url.split('.')
			parts[-2] += modifier
			return '.'.join(parts)
		else:
			return url
	
	# set the correct thumbnail URL from imgur
	for image in data['images'][:1]:
		image['thumb_url'] = image['url']	
	for image in data['images'][1:4]:
		image['thumb_url'] = thumb_url(image['url'], 'l')
	for image in data['images'][4:]:
		image['thumb_url'] = thumb_url(image['url'], 'm')

	# constructs a tree data structure for the template to 
	# convert into HTML for the correct layout
	def img(i):
		if i >= len(data['images']):
			return None
		return data['images'][i]

	def col_imgs(offset):
		i = offset
		while i < len(data['images']):
			yield data['images'][i]
			i += 5

	data['images'] = [[img(0),[img(3),list(col_imgs(8)),list(col_imgs(9))],[img(4),list(col_imgs(7))]],
					[img(1),img(2),list(col_imgs(5)),list(col_imgs(6))]]

	if 'user' in data and data['user']['id'] == data['topic']['creator_id']:
		data['user']['is_creator'] = True
	#return data['images']
	return render('topic-page', data)

def render_error(error_message):
	data = {'error_message': error_message}
	return render('error', data)