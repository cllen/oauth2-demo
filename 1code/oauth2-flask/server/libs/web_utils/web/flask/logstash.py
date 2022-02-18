import traceback
from functools import wraps
import logging

from flask import request,current_app,g
from flask_restx.reqparse import RequestParser

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from .exceptions.base import BaseHTTPException
from ...logger.logstash.get_logger import get_logstash_logger

class Logstash:

	def __init__(self,app=None):
		if app:
			self.init_app(app)

	def init_app(self,app):
		@app.after_request
		def after_request(response):
			from flask import g
			if hasattr(g,'logstash'):
				g.logstash.update({
					'http_code':response.status_code,
				})
				
				logger = get_logstash_logger(level=logging.INFO)
				if app.config['TESTING'] != True:
					if g.logstash_level == 'info':
						logger.info(msg="success",extra=g.logstash)
					else:
						logger.error(msg="error",extra=g.logstash)
			return response

def logstash_api(api_name):

	def wrapper1(func):

		# @wraps(func)
		def wrapper2(*args, **kwargs):

			g.logstash = {}
			g.logstash_level = 'info'

			g.logstash.update({
				'http_authorization': request.environ.get('HTTP_AUTHORIZATION'),
				'api_name':api_name,
				'api_url':request.path,
				'arguments':request.get_json()
			})
			if hasattr(request,'user'):
				g.logstash.update({
					'user_openid':request.user.openid,
					'user_nickname':request.user.nickname,
				})

			try:
				result = func(*args, **kwargs)

				errcode = result['errcode'] if isinstance(result,dict) else 0
				g.logstash.update({
					'errcode':errcode,
				})
				
			except Exception as e:
				g.logstash_level = 'error'
				if issubclass(e.__class__,BaseHTTPException):
					g.logstash.update({
						'http_code':e.code,
						'errcode':e.errcode,
						'error_message':e.message,
					})
				else:
					g.logstash.update({
						'http_code':500,
						'errcode':-1,
						'error_traceback':traceback.format_exc(),
					})

				raise e

			return result
		return wrapper2
	return wrapper1





