from inspect import isfunction
import re

def check(self, value, error_response, status=400):
	if value:
		return value
	else:
		if isfunction(error_response):
			error_response()
			raise AssertionError('Check failed')
		else:
			self.response.status = status
			self.response.write(view.render_error(error_response))
			raise AssertionError('Check failed. ' + error_response)

def urlify(name):
	# split into list of words
	words = name.strip().lower().split(' ')
	# remove non-alphanumeric chars from each word
	words = map(lambda s: re.sub(r'\W', '', s), words)
	# remove empty strings
	words = [word for word in words if word]
	# join words with a dash
	return str('-'.join(words))