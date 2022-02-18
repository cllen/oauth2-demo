from libs.web_utils.meta import Singleton
from libs.web_utils.settings import BaseSettings

class Settings(BaseSettings,metaclass=Singleton):

	default = {
		'client_id':"",
		'client_secret':'',

		'redis_db':0,
		'redis_host':'localhost',
		'redis_port':6379,
		'redis_password':None,

		# 'access_token_expiration':60 * 60 * 24 * 7,

		# 课程管理系统的api
		'client_default_uri':'{}/cms/home'.format('http://localhost:5000'), # 课程管理页面首页
		'client_code2token_api':'{}/cms/token'.format('http://localhost:5000'), # 课程管理系统得到code后，获取token

		# 授权的四种方式
		'authorization_code_api':'{}/oauth2/authorization/authorize'.format('http://localhost:5001'), # 获取code的api
		# 'implict_api':'{}/oauth2/authorization/authorize'.format('http://localhost:5001'), # 隐式登录的api（这里应该用不到）
		# 'resource_owner_password_api':'{}/oauth2/authorization/token'.format('http://localhost:5001'), # 密码登录的api（这里应该用不到）
		# 'client_credentials_api':'{}/oauth2/authorization/token'.format('http://localhost:5001'), # 口令登录的api（这里应该用户到）

		# 服务器后端请求
		'code2token_api':'{}/oauth2/authorization/token'.format('http://oauth2_authorization:5000'), # 统一登录系统的code2token接口
		'token2userinfo_api':'{}/oauth2/resource/api/v1/oauth2/user'.format('http://oauth2_resource:5000'), # 统一登录系统的用户信息获取接口
	}
