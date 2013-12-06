import webapp2
import logging
from google.appengine.api import users
import datastore
import view_renderer as view
import difflib

class HomeHandler(webapp2.RequestHandler):
	def homepage(self):
		user = users.get_current_user()
		page_data = dict()
		if user:
			page_data['user'] = {
				'name': user.nickname(),
				'id': user.user_id()
			}

		self.response.write(view.render('home-page', page_data))

	def search(self):
		query = self.request.get('query')
		index = datastore.SearchIndexShard.build_index()
		url_dict = dict()
		for pair in index:
			# self.response.write(str(pair) + '<br>')
			if pair[1] in url_dict:
				url_dict[pair[1]].append(pair[0])
			else:
				url_dict[pair[1]] = [pair[0]]
		names = [x[1] for x in index]
		
		matches = difflib.get_close_matches(query, names, 50, 0.5)
		for name in names:
			if query.lower() in name.lower() and name not in matches:
				matches.append(name)
		page_data = {
			'search_results': list(),
			'query': query
		}
		for match in matches:
			for url in url_dict[match]:
				page_data['search_results'].append({'url': url, 'name': match})

		user = users.get_current_user()
		if user:
			page_data['user'] = {
				'name': user.nickname(),
				'id': user.user_id()
			}

		self.response.write(view.render('search-results', page_data))