class Config:
 	# general config
  	SECRET_KEY = "\xfb5\xa7\x90$\x9f\xcf\xfc\xab\x8a\xa1\xdd9\xf9|\xb3\xe3\xd9\xc0O;\x960"
  	DEBUG = True
  	ENV = "production"
  	SESSION_COOKIE_SAMESITE = "lax"
  	# SERVER_NAME = ""
  
  	# database config
  	SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
  	SQLALCHEMY_ECHO = True
  	SQLALCHEMY_TRACK_MODIFICATIONS = False