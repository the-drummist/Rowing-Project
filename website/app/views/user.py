from flask import Blueprint, render_template, redirect, url_for, request
from app.models import db, User

user = Blueprint(name = 'user', import_name = __name__, static_folder = "/app/static", template_folder = "/app/templates")
