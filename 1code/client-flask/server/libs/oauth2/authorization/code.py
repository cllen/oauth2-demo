from ..utils.crypt import Crypt

class Code:

	def __init__(self,
		secret_key=None,
		salt=None,
		expire_in=None,
	):
		if None not in [secret_key,salt,expire_in]:
			self.init(secret_key,salt,expire_in)

	def init(self,
		secret_key,
		salt,
		expire_in,
	):
		self.secret_key = secret_key
		self.salt = salt
		self.expire_in = expire_in

	def issue(self,client_id,user_id,scope:str):
		code =  Crypt.encrypt({
			'client_id':client_id,
			'user_id':user_id,
			'scope':scope,
		},self.secret_key,self.salt,self.expire_in)

		return code

	def verify(self,code):

		data = Crypt.decrypt(code,self.secret_key,self.salt,self.expire_in)

		return data
