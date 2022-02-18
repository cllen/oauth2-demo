
class Scope:
	snsapi_base = 0x01 * 2 ** 0
	snsapi_userinfo = 0x01 * 2 ** 1

class ResponseType:
	code = 'code'
	token = 'token'

class GrantType:
	authorization_code = 'authorization_code'
	implicit = 'implicit'
	resource_owner_password_credentials = 'resource_owner_password_credentials'
	client_credentials = 'client_credentials'
