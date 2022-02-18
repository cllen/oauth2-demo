import logging
logging.basicConfig(level=logging.DEBUG)
import traceback

from flask import (
	request, 
	render_template, 
	redirect, 
	current_app, 
	session, 
	flash
)
from flask_restx import Resource

from flask_cors import cross_origin

from . import (
	bp,
	api,
)

from libs.oauth2.utils.constants import Scope

# ns = api.namespace('resource')
