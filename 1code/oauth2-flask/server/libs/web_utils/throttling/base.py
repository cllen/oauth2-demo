import time
import abc
import json
from ..redis.base import BaseRedis
from ..constans import RedisKeys

import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

class HistorysList:

	def __init__(self,
		remote_addr,
		throttling_api_url,

		redis_host,
		redis_port,
		redis_db,
		redis_password
	):
		self.__remote_addr = remote_addr
		self.__key = RedisKeys.throttle.format(self.__remote_addr,throttling_api_url)
		self.__expires_in = 60*2
		self.__redis = BaseRedis(
			host=redis_host,
			port=redis_port,
			db=redis_db,
			password=redis_password,
		)
		self.data = self.__get_list()

	def insert(self,index,value):
		result = self.data.insert(index,value)
		self.__update_redis()
		return result

	def pop(self):
		element = self.data.pop()
		self.__update_redis()
		return element

	def __iter__(self):
		return iter(self.data)

	def __len__(self):
		return len(self.data)

	def __getitem__(self,name):
		return self.data[name]

	def __get_list(self):
		value = self.__redis.get(self.__key)
		if value:
			return json.loads(value)
		else:
			return []

	def __update_redis(self):
		self.__redis.set(
			self.__key,
			self.__expires_in,
			json.dumps(self.data)
		)


class BaseThrottle:

	def __init__(self,

		remote_addr,
		throttling_api_url,
		limit_historys=60,
		term=60,

		redis_host='127.0.0.1',
		redis_port=6379,
		redis_db=0,
		redis_password=None

	):

		self.remote_addr = remote_addr
		self.throttling_api_url = throttling_api_url
		self.limit_historys = limit_historys
		self.term = term

		self.historys = HistorysList(
			self.remote_addr,
			self.throttling_api_url,

			redis_host=redis_host,
			redis_port=redis_port,
			redis_db=redis_db,
			redis_password=redis_password
		)

	def is_allow(self):
		ctime = time.time()
		while self.historys.data and self.historys[-1] < ctime-self.term:
			self.historys.pop()
		if len(self.historys)<self.limit_historys:
			self.historys.insert(0,ctime)
			return True
		else:
			return False

	def wait(self):
		ctime = time.time()
		#logger.info(self.historys)
		return self.term-(ctime-self.historys[-1])

