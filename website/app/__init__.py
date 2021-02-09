from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
  app = Flask(__name__, instance_relative_config=False)
  app.config.from_object('config.Config')

  
  db.init_app(app)
  with app.app_context():
    from app.views import info, user
      # Register blueprints
    app.register_blueprint(info.info)
    app.register_blueprint(user.user)
    db.create_all()
    return app
