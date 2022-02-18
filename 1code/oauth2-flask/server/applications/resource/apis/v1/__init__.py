from flask import Blueprint
from flask_restx import Api

bp = Blueprint('resource-api',__name__)

api = Api(bp)

from . import (
	user,
)