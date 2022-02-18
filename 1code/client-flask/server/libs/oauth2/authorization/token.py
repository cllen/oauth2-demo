from ..utils.crypt import Crypt

class Token:

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

		refresh_token_expires_in = self.expire_in*2
		
		access_token =  Crypt.encrypt({
			'client_id':client_id,
			'user_id':user_id,
			'scope':scope,
		},self.secret_key,self.salt,self.expire_in)

		refresh_token =  Crypt.encrypt({
			'client_id':client_id,
			'user_id':user_id,
			'scope':scope,
		},self.secret_key,self.salt,refresh_token_expires_in)



		return access_token,refresh_token,self.expire_in,refresh_token_expires_in

	def verify(self,token):

		data = Crypt.decrypt(token,self.secret_key,self.salt,self.expire_in)

		return data
