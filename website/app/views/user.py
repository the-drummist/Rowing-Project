from flask import Blueprint, render_template, redirect, url_for, request
from app.models import db, User
from app.data_analysis import Data

user = Blueprint(name = 'user', import_name = __name__, static_folder = "/app/static", template_folder = "/app/templates")

### SECTION: Session Related Routes ###
@user.route("/register",methods=[ "GET", "POST"])
def register():
	pass

@user.route("/login", methods=["GET", "POST"])
def login():
	pass

@user.route("/logout", methods=["GET"])
def logout():
	pass
### END SECTION ###

### SECTION: Main Routes ###
@user.route("/dashboard/<username>", methods=["GET"])
def dashboard(username):
	pass

@user.route("/account/settings", methods=["GET", "POST"])
def settings():
	pass

@user.route("/account/upload", methods=["GET", "POST"])
def upload():
	pass

@user.route("/upload/<username>", methods=["POST"])
def autoUpload(username):
	pass