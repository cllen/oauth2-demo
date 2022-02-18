from werkzeug.http import parse_authorization_header
from .exceptions import (
	AuthorizationErrorTypeException,
	AuthorizationErrorUsernameOrPasswordException,
	AuthorizationErrorUnAuthorizationException
)

class Authorization:

	def __init__(self,
		environ,
		username,
		password,
		realm=''
	):
		self.environ = environ
		self.username = username
		self.password = password
		self.realm = realm

	def authenticate(self):

		field_value = self.environ.get('HTTP_AUTHORIZATION')

		authorization = parse_authorization_header(field_value)

		# from flask import request
		# authorization = request.authorization

		if not authorization:
			raise AuthorizationErrorUnAuthorizationException('authorization field not found!')

		if authorization.type != 'basic':
			raise AuthorizationErrorTypeException('Error Authorization type!')

		if authorization.username != self.username or \
			authorization.password != self.password:
			raise AuthorizationErrorUsernameOrPasswordException('Error username or password!')

		return True

	def challenge(self):
		return 401,{'WWW-Authenticate': 'Basic realm="%s"' % self.realm}
