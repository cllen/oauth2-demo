from flask_restx import reqparse

Get = reqparse.RequestParser()
Get.add_argument('client_id', type=str, required=True)
Get.add_argument('client_secret', type=str, required=True)
Get.add_argument('user_access_token', type=str, required=True)

from marshmallow import Schema, fields, ValidationError
