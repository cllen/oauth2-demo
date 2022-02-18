from sqlalchemy import Column, String, Integer, Boolean

from applications import db

class Client(db.Model):
	__tablename__ = 'oauth2_client'
	# __abstract__ = True
	# __table_args__ = {"useexisting": True}

	id = Column(Integer, primary_key=True)
	client_id = Column(String(200))
	client_secret = Column(String(200))
	client_name = Column(String(200))
	scope = Column(Integer)

	def to_dict(self):
		return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
