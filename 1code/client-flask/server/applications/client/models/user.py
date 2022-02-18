from sqlalchemy import Column, String, Integer, Boolean
from applications import db

class User(db.Model):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	oauth2_user_id = Column(Integer, primary_key=True)
	account = Column(String(256), primary_key=True)
	username = Column(String(256))
	type = Column(String(256))

	# 这里只存储用户信息，其他信息就在其他表里面直接存一个oauth2_user_id


	def __str__(self):
		return "{},{},{}".format(self.account,self.username,self.type)