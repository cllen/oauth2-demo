from flask import Blueprint

bp = Blueprint('authorization-view',__name__)

from . import (
	authorize,
)