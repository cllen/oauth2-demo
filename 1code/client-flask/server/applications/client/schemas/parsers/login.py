from marshmallow import Schema, fields


class CodeCallback(Schema):
	code = fields.Str(required=True)

class GetToken(Schema):
	error_code = fields.Integer(required=True)
	error_message = fields.Str()
	access_token = fields.Str()
	refresh_token = fields.Str()
	access_token_expires_in = fields.Integer()
	refresh_token_expires_in = fields.Integer()
	

class User(Schema):
	id = fields.Integer()
	account = fields.Str()
	username = fields.Str()
	type = fields.Str()

class GetUserinfo(Schema):
	error_code = fields.Integer(required=True)
	error_message = fields.Str(required=False, allow_none=True)
	error_detail = fields.Str(required=False, allow_none=True)
	entry = fields.Nested(User, allow_none=True)


