class Config:
 	# general config
  	SECRET_KEY = "\xfb5\xa7\x90$\x9f\xcf\xfc\xab\x8a\xa1\xdd9\xf9|\xb3\xe3\xd9\xc0O;\x960"
  	DEBUG = True
  	ENV = "production"
  	SESSION_COOKIE_SAMESITE = "lax"
  	# SERVER_NAME = ""
  
  	# database config
  	SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
  	# production db uri
  	# SQLALCHEMY_DATABASE_URI = 'postgres://qolduouvyfddse:95733d22eb98d763f799900278ca019d7ca99ba25b8e1bbbfd311e4fef65e47a@ec2-54-167-168-52.compute-1.amazonaws.com:5432/d5mhj6udvnh3cs'
  	SQLALCHEMY_ECHO = True
  	SQLALCHEMY_TRACK_MODIFICATIONS = False