from marshmallow import Schema, fields

class Get(Schema):
	scope = fields.Str(required=True)
	client_id = fields.Str(required=True)
	redirect_uri = fields.Str(required=True)
	response_type = fields.Str(required=True)

class Post(Schema):
	account = fields.Str(required=True)
	password = fields.Str(required=True)

	response_type = fields.Str(required=True)
	client_id = fields.Str(required=True)
	redirect_uri = fields.Str(required=True)
	scope = fields.Str(required=True)
	# state = fields.Str(required=True)
	# grant_type = fields.Str(required=True)

class GetToken(Schema):
	code = fields.Str(required=True)
	grant_type = fields.Str(required=True)
	client_id = fields.Str(required=True)
	client_secret = fields.Str(required=True)
