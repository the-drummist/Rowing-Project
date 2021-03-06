from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User
from app.data_analysis import Data
from app.helper import login_required, generate_key

user = Blueprint(name = 'user', import_name = __name__, static_folder = '/app/static', template_folder = '/app/templates')

### SECTION: Session Related Routes ###
@user.route('/register',methods=[ 'GET', 'POST'])
def register():
	if request.method == 'POST':
		# get user form attributes
		email = request.form.get('email')
		username = request.form.get('username')
		password = request.form.get('password')
		# generate password hash
		password_hash = generate_password_hash(password)
		# generate an upload key
		key = generate_key()
		# create the new user and add it to the database
		new_user = User(username=username, email=email, hash=password_hash, upload_id=key)
		db.session.add(new_user)
		db.session.commit()
		# get the users id to add it to the sessions
		user = User.query.filter_by(username).first()
		# just including this if to avoid potential security vulnerabilities 
		if user and check_password_hash(user.hash, password):
			session['user_id'] = user.id
		return redirect(url_for('setup'))
	if request.method == 'GET':
		return render_template('register.html')

@user.route('/login', methods=['GET', 'POST'])
def login():
	# clear any sessions
	session.clear()
	# if the user makes a post request
	if request.method == 'POST':
		# get the users username and password
		username = request.form.get('username')
		password = request.form.get('password')
		# make sure data is present
		if not username or not password:
			flash('Must provide your username and password')
			return render_template('login.html')
		# if the data is present query the database and check their password
		else:
			user = User.query.filter_by(username).first()
			if user and check_password_hash(user.hash, password):
				# add the user to the sessions list
				session['user_id'] = user.id
			else:
				# warn the user of incorrect username or password
				flash('incorrect username or password')
				return render_template('login.html')

	# if the user makes a get request, return the login template
	if request.method == 'GET':
		return render_template('login.html')
			
@user.route('/account/setup', methods=['GET', 'POST'])
@login_required
def setup():
	if request.method == 'POST':
		# get form attributes 
		birthday = request.form.get('birthday')
		sex = request.form.get('sex')
		weight = request.form.get('weight')
		rhr = request.form.get('rhr')
		# get and update the users row in the database with new info
		user = User.query.filter_by(session['user_id']).first()
		user.birthday = birthday
		user.sex = sex
		user.weight = weight
		user.rhr = rhr
		db.session.commit()
		return redirect('dashboard')

	if request.method == 'GET':
		user = db.query.filter_by(session['user_id']).first()
		# return the user object so that the values that do exist can be used as placeholders.
		return render_template('setup.html', user=user)

@user.route('/logout', methods=['GET'])
@login_required
def logout():
	# clear the session
	session.clear()
	# redirect the user to the login page
	return redirect(url_for('login'))

### END SECTION ###

### SECTION: Main Routes ###
@user.route('/dashboard/<username>', methods=['GET'])
@login_required
def dashboard(username):
	user = db.query.filter_by(session['user_id']).first()
	username = user.username
	



@user.route('/account/settings', methods=['GET', 'POST'])
@login_required
def settings():
	if request.method == 'POST':
		return 'under construction, try again soon'
	if request.method == 'GET':
		return 'under construction, try again soon'

@user.route('/account/upload', methods=['GET', 'POST'])
@login_required
def upload():
	if request.method == 'POST':
		return 'under construction, try again soon'
	if request.method == 'GET':
		return 'under construction, try again soon'


@user.route('/upload/<username>', methods=['POST'])
def autoUpload(username):
	return