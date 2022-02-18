from flask_restx import Model,fields
from applications.resource.apis.v1 import api

User = api.model(
	'User',
	{
		'id':fields.Integer(),
		'username':fields.String(),
		'account':fields.String(),
		'type':fields.String(),
	}
)

Get = api.model(
	'GetUser',
	{
		'error_code':fields.Integer(),
		'error_message':fields.String(),
		'error_detail':fields.String(),
		'error_detail2':fields.String(),
		'entry':fields.Nested(User),
	}
)


