from functools import wraps
from flask import request
from ...throttling.base import BaseThrottle
from .exceptions.throttling import ThrottlingException

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def throttling(
	limit=60,
	term=60,

	redis_host='localhost',
	redis_port=6397,
	redis_db=0,
	redis_password=None
	):

	def wrapper1(func):

		def wrapper2(*args, **kwargs):
			# from pprint import pprint
			# pprint(request.__dict__)

			func1 = func

			throttle = BaseThrottle(
				remote_addr=request.environ['REMOTE_ADDR'],
				throttling_api_url=request.environ['PATH_INFO'], # REQUEST_URI
				limit_historys=limit,
				term=term,

				redis_host=redis_host,
				redis_port=redis_port,
				redis_db=redis_db,
				redis_password=redis_password
			)

			is_allow = throttle.is_allow()
			if not is_allow:
				wait_time = int(throttle.wait())
				raise ThrottlingException(
					errcode=109799,
					message='Access frequency is limited,please wait {} seconds!'.format(wait_time)
				)

			return func1(*args, **kwargs)

		return wrapper2
	return wrapper1
