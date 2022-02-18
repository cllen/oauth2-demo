from sqlalchemy import Column, String, Integer, Boolean

from applications import db

class Configuration(db.Model):
	__tablename__ = 'oauth2_configuration'
	# __abstract__ = True
	# __table_args__ = {"useexisting": True}

	id = Column(Integer, primary_key=True)
	redis_db = Column(String(200))
	redis_host = Column(String(200))
	redis_port = Column(Integer)
	redis_password = Column(String(200))

	token_secret_key = Column(String(200))
	token_salt = Column(String(200))
	token_expiration = Column(Integer)

	def to_dict(self):
		return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
