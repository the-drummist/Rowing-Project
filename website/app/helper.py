from functools import wraps
from flask import url_for, redirect
def login_required(f):
	"""
	Decorate routes to require login.

	http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
	"""
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get('user_id') is None:
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function

def generate_key():
	pass

def validate_key():
	pass