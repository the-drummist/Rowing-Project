from flask import Blueprint, render_template

info = Blueprint(name = 'info', import_name = __name__, static_folder = "/app/static", template_folder = "/app/templates")

@info.route("/home", methods=["GET"])
@info.route("/", methods=["GET"])
def index():
	return render_template("index.html")

@info.route("/<string:filename>", methods=["GET"])
def dynamic_index(filename):
	filename = filename +".html"
	return render_template(filename)