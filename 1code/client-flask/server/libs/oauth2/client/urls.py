
class Urls:

	"""
		grant type
	"""
	@staticmethod
	def authorization_code(
		authorization_code_api,
		client_id,
		code_callback_api,
		scope,
	):	
		url = "{}?response_type=code&client_id={}&redirect_uri={}&scope={}".format(
			# 通常是：https://oauth2.com/oauth2/authorize
			authorization_code_api,
			client_id,
			code_callback_api,
			scope
		)
		return url

	@staticmethod
	def implict(
			implict_api,
			client_id,
			token_callback_api,
			scope
	):
		url = "{}?response_type=token&client_id={}&redirect_uri={}&scope={}".format(
			
			# 通常是： https://oauth2.com/oauth2/authorize
			implict_api,
			client_id,
			token_callback_api,
			scope
		)

		return url

	# 使用用户的账号密码获取token，用于当第三方要在统一登录系统要使用用户的特殊功能时候，token作为临时凭证，可以用到。
	# 一般不使用这种方法
	@staticmethod
	def password(password_api,username,password,client_id):
		url = "{}?grant_type=password&username={}&password={}&client_id={}".format(
			# 通常是：https://oauth2.com/oauth2/token
			password_api,
			username,
			password,
			client_id
		)

		return url

	# 使用第三方的账号密码获取token，用于党用户在统一登录系统要使用第三方的特殊功能时候，token作为临时凭证，可以用到。
	# 一般使用这种方法
	@staticmethod
	def credentials(
		client_credentials_api,
		client_id,
		client_secret
	):
		# 使用第三方的账号密码获取token，与用户无关。
		url = "{}?grant_type=client_credentials&client_id={}&client_secret={}".format(
			# 通常是：https://oauth2.com/oauth2/token
			client_credentials_api,
			client_id,
			client_secret
		)

		return url


	# 第三方在后端用code换取token
	@staticmethod
	def get_token(
		token_api,
		client_id,
		client_secret,
		grant_type,
		code,
	):
		url = "{}?&client_id={}&client_secret={}&grant_type={}&code={}".format(
			# 通常是：https://oauth2.com/oauth2/token
			token_api,
			client_id,
			client_secret,
			grant_type,
			code
		)
		return url

	# 第三方在后端用token换取用户信息
	@staticmethod
	def get_userinfo(
		userinfo_api,
		client_id,
		client_secret,
		user_access_token
	):
		url = "{}?client_id={}&client_secret={}&user_access_token={}".format(
			# 通常是：https://oauth2.com/oauth2/user
			userinfo_api,
			client_id,
			client_secret,
			user_access_token
		)
		return url