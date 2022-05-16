

class Config:
	SECRET_KEY = ''
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = ''
	JSON_AS_ASCII = False
	GOOGLE_OAUTH2_CLIENT_ID = ''
	GOOGLE_OAUTH2_SECRET = ''
	GOOGLE_DISCOVERY_URL = 'http://localhost:8000/home'
	FACEBOOK_OAUTH2_CLIENT_ID = ''
	FACEBOOK_OAUTH2_CLIENT_SECRET = ''
	TWITTER_CLIENT_ID = ''
	TWITTER_CLIENT_SECRET = ''
	  
	PASSWORD_COMPLEX_PATTER = r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[~.!@#$%^&*()_\-+|{}\[\];:'\",<>\?/]).*"
	MINIMUM_PASSWORD_LENGTH = 8

	MAIL_DEFAULT_SENDER = ''
	MAIL_DEFAULT_SENDER_PASSWORD = ""
	SEND_ERROR_MSG_BY_EMAIL = False
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = "587"

	USER_DEFAULT_ACTIVE_STATE = 0
	USER_START_ACTIVE_STATE = 1
	

class DevelopmentConfig(Config):
    pass

config = {
    'default': DevelopmentConfig
}

