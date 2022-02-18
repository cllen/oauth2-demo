from sqlalchemy import Column, String, Integer, Boolean

from applications import db

from applications.authorization.utils.constants import UserType

class User(db.Model):
	__tablename__ = 'oauth2_user'
	# __abstract__ = True
	# __table_args__ = {"useexisting": True}

	id = Column(Integer, primary_key=True)
	username = Column(String(200))
	password = Column(String(200))
	account = Column(String(200))
	type = Column(String(200), default=UserType.student)

	def to_dict(self):
		return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
