from libs.web_utils.meta import Singleton
from libs.web_utils.settings import BaseSettings

class Settings(BaseSettings,metaclass=Singleton):
	"""
		oauth2 settings
	"""
	default = {
		'token_secret_key':'xxx',
		'token_salt':'xxx',
		'token_expiration':60*60*24*7,

		'redis_db':0,
		'redis_host':'xxx',
		'redis_port':6379,
		'redis_password':'',
		'access_token_expiration':60*60*2,
	}