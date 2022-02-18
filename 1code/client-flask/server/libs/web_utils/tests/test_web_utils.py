import os
import time
import base64
import unittest

from ..logger import get_logstash_logger
from ..permission.base import BasePermission
from ..permission.defs import ExamplePermissions
from ..redis.base import BaseRedis
from ..throttling.base import BaseThrottle

import requests
from flask import Flask
from ..web.flask import (
	authorization,basichttp_required,gen_basichttp_header,
	permission,
	throttling,
	logstash_api,
	Logstash,
)

logstash = Logstash()


class BaseTestCase(unittest.TestCase):
	
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_logstash(self):

		logger = get_logstash_logger()

		logger.info({})

	def test_permission(self):

		user_permission = ExamplePermissions.USER

		is_can = BasePermission.can(
			user_permission=user_permission,
			required_permission=ExamplePermissions.USER
		)
		self.assertEqual(is_can,True)

		is_can = BasePermission.can(
			user_permission=user_permission,
			required_permission=ExamplePermissions.ADMINISTER
		)
		self.assertEqual(is_can,False)

		user_permission = BasePermission.add(
			current_permission=user_permission,
			additional_permission=ExamplePermissions.ADMINISTER
		)

		is_can = BasePermission.can(
			user_permission=user_permission,
			required_permission=ExamplePermissions.USER
		)
		self.assertEqual(is_can,True)

		is_can = BasePermission.can(
			user_permission=user_permission,
			required_permission=ExamplePermissions.ADMINISTER
		)
		self.assertEqual(is_can,True)

	def test_redis(self):
		redis = BaseRedis(
			host='localhost',
			port=16379,
			db=0,
			password=None
		)
		key = 'test_redis'
		expires_in = 1
		value = redis.get(key)
		self.assertEqual(value,None)
		target_value = 'yes'
		redis.set(key,expires_in,target_value)
		value = redis.get(key)
		self.assertEqual(value,target_value)
		time.sleep(expires_in*2)
		value = redis.get(key)
		self.assertEqual(value,None)

	def test_throttling(self):
		throttle = BaseThrottle(
			remote_addr='127.0.0.1',
			throttling_api_url='test api',
			limit_historys=3,
			term=1,

			redis_host='localhost',
			redis_port=16379,
			redis_db=0,
			redis_password=None
		)

		is_allow = throttle.is_allow()
		self.assertEqual(is_allow,True)

		is_allow = throttle.is_allow()
		self.assertEqual(is_allow,True)

		is_allow = throttle.is_allow()
		self.assertEqual(is_allow,True)

		is_allow = throttle.is_allow()
		self.assertEqual(is_allow,False)

		time.sleep(1)

		is_allow = throttle.is_allow()
		self.assertEqual(is_allow,True)

class WebTestCase(unittest.TestCase):

	def setUp(self):
		self.app = Flask(__name__)	
		logstash.init_app(self.app)

	def tearDown(self):
		pass

	def test_basichttp_required(self):
		
		@self.app.route('/basichttp')
		# @logstash_api('管理员首页')

		@basichttp_required(username="admin",password="admin")
		# @authorization(
		# 	auths={
		# 	}
		# )
		# @permission(
		# 	requireds=[ExamplePermissions.ADMINISTER,]
		# )
		# @throttling(
		# 	limit=3,
		# 	term=1,
		# 	redis_host='localhost',
		# 	redis_port=16397,
		# 	redis_db=0,
		# 	redis_password=None
		# )
		def home():
			return 'admin page'

		self.client = self.app.test_client(use_cookies=True)

		response = self.client.get('/basichttp')
		self.assertEqual(int(response.status.split(' ')[0]),401)

		headers = gen_basichttp_header(username='admin',password='test')
		response = self.client.get('/basichttp',headers=headers)
		self.assertEqual(int(response.status.split(' ')[0]),401)

		headers = gen_basichttp_header(username='admin',password='admin')
		response = self.client.get('/basichttp',headers=headers)
		self.assertEqual(int(response.status.split(' ')[0]),200)

		# self.app.run()

	def test_logstash(self):
		
		@self.app.route('/logstash')
		@logstash_api('测试页面')
		def home():
			return 'test page'

		self.client = self.app.test_client(use_cookies=True)

		response = self.client.get('/logstash')

	def test_throttling(self):

		@self.app.route('/throttling')
		@throttling(
			limit=3,
			term=1,
			redis_host='localhost',
			redis_port=16379,
			redis_db=0,
			redis_password=None
		)
		def home():
			return 'throttling page'

		self.client = self.app.test_client(use_cookies=True)

		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),200)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),200)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),200)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),400)
		time.sleep(1)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),200)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),200)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),200)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),400)
		time.sleep(1)
		response = self.client.get('/throttling')
		self.assertEqual(int(response.status.split(' ')[0]),200)