from flask import Blueprint, render_template

info = Blueprint(name = 'info', import_name = __name__, static_folder = "/app/static", template_folder = "/app/templates")