import abc
from ..meta import Singleton

class BaseSettings:

	"""
		同理auth，将miniorm设置为变量，使用了控制反转技巧。
	"""

	# This attribute needs to be override.
	default = {}

	miniorm = None
	instance = None
	settings_cls = None

	def __init__(self,
		miniorm=None,
		settings_cls = None,
		default={}
	):

		if default:
			self.default = default
		if miniorm:
			self.miniorm = miniorm
		if settings_cls:
			self.settings_cls = settings_cls

	def __getattr__(self,key):
		self.instance = self.miniorm(self.settings_cls).first()
		if self.instance:
			return getattr(self.instance,key) or self.default.get(key,0)
		else:
			return self.default.get(key,0)

	def __setattr__(self,key,value):
		if key in ['default','miniorm','instance','settings_cls']:
			return super().__setattr__(key,value)
		else:
			self.instance = self.miniorm(self.settings_cls).first()
			if self.instance:
				self.miniorm(self.settings_cls).update(instance=self.instance,**{key:value})
			else:
				self.miniorm(self.settings_cls).save(**{key:value})
			self.instance = self.miniorm(self.settings_cls).first()
			return self.instance

	def update(self,**kwargs):
		self.instance = self.miniorm(self.settings_cls).first()
		if self.instance is not None:
			self.miniorm(self.settings_cls).update(instance=self.instance,**kwargs)
		else:
			self.miniorm(self.settings_cls).save(**kwargs)
		self.instance = self.miniorm(self.settings_cls).first()
		return self.instance

class WechatSettings(BaseSettings,metaclass=Singleton):
	default = {
		'appid':'xxx',
		'app_secret':'xxx',
		'app_category':'miniapp',
		'mch_id':'xxx',
		'mch_secret':'xxx',

		'token_secret_key':'xxx',
		'token_salt':'xxx',
		'token_expiration':60*60*24*7,
		
		'redis_db':0,
		'redis_host':'xxx',
		'redis_port':6379,
		'redis_password':'',
		'access_token_expiration':60*60*2,
		
		'oauth_redirect_url':'xxx',
		'post_oauth_redirect_url_default':'xxx',
		'oauth_redirect_token_expiration':60*60*24*365,
		'mp_token':'xxx',
	}