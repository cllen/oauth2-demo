from functools import wraps
import base64
from flask import request
from werkzeug.exceptions import HTTPException
from .exceptions.authorization import AuthorizationException

from ...authorization.basic_http import Authorization
from ...authorization.exceptions import (
	AuthorizationErrorTypeException,
	AuthorizationErrorUsernameOrPasswordException,
	AuthorizationErrorUnAuthorizationException,
)

import time
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def authorization(
	auths={},
):

	def wrapper1(func):

		@wraps(func)
		def wrapper2(*args,**kwargs):

			func1 = func

			authorization = request.environ.get('HTTP_AUTHORIZATION') or " "
			if not authorization:
				raise AuthorizationException(109999)

			credentials_type,credentials = authorization.split(' ')

			auth = auths.get(credentials_type,None)

			if not auth:
				raise AuthorizationException(109998)
			
			func1 = auth(func1)

			return func1(*args,**kwargs)

		return wrapper2

	return wrapper1


def basichttp_required(username,password):
	def wrapper2(func):

		@wraps(func)
		def wrapper3(*args,**kwargs):

			from flask import request,Response

			auth = Authorization(
				environ=request.environ,
				username=username,
				password=password,
			)

			try:
				is_passed = auth.authenticate()
				print(is_passed)
			except Exception as e:
				http_status,http_header = auth.challenge()
				return Response(status=http_status,headers=http_header)

			return func(*args,**kwargs)

		return wrapper3
	return wrapper2

def gen_basichttp_header(username,password):
	byte_base64 = base64.b64encode("{}:{}".format(username,password).encode("utf-8"))
	return {'authorization':"basic "+byte_base64.decode("utf-8")}
