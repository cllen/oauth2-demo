from sqlalchemy import Column, String, Integer, Boolean
from applications import db

class Configuration(db.Model):
	__tablename__ = 'configuration'

	id = Column(Integer, primary_key=True, autoincrement=True)
	client_id = Column(Integer)
	client_secret = Column(String(2000))

	redis_db = Column(String(2000))
	redis_host = Column(String(2000))
	redis_port = Column(Integer)
	redis_password = Column(String(2000))

	# 课程管理系统的地址
	client_default_uri = Column(String(2000))
	client_code2token_api = Column(String(2000))

	# 授权的四种方式
	authorization_code_api = Column(String(2000))
	# implict_api = Column(String(2000))
	# resource_owner_password_api = Column(String(2000))
	# client_credentials_api = Column(String(2000))
	#register_api = Column(String(2000))

	# 服务器后端请求
	code2token_api = Column(String(2000))
	token2userinfo_api = Column(String(2000))
	
	def to_dict(self):
		return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

