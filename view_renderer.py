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

	for large_image in data['images'][:4]:
		large_image['thumb_url'] = large_image['url']
	data['images'] = [[img(0),[img(3),list(col_imgs(8)),list(col_imgs(9))],[img(4),list(col_imgs(7))]],
					[img(1),img(2),list(col_imgs(5)),list(col_imgs(6))]]

	#return data['images']
	return render('topic-page', data)