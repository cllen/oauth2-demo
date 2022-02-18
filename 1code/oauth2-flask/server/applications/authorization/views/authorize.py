from ._imports_ import *
logger = logging.getLogger(__name__)

# 自己的库
from libs.web_utils.permission.base import BasePermission
from libs.oauth2.utils.constants import (
	Scope,
	ResponseType,
	GrantType
)

from libs.oauth2.authorization import (
	Code,Token
)



# 业务代码

from ..schemas.parsers.authorize import (
	Get as GetSchema,
	Post as PostSchema,
	GetToken as GetTokenSchema,
)

from ..models import (
	Client as ClientModel,
	User as UserModel,
)

from exceptions import (
	error_messages,
	UserNotFound,
	ClientNotFound,
	ScopeNotExisted,
	ScopeNotAllowed,
	IssueCodeError,
	IssueTokenError,
	ResponseTypeNotExisted,
)

# 实例化


@bp.route('/authorize', methods=['GET','POST'])
def authorize():
	
	# 请求登录页面
	if request.method == 'GET':
		
		# 参数反序列化
		try:
			params = GetSchema().load(request.values)
		except Exception as e:
			# 参数错误 
			return render_template(
				'home/error.html',
				data={
					'http_code':400,
					'error_code':1001,
					'error_message':error_messages[1001],
					'error_detail':str(e)
				}
				
			), 400

		# 判断是否存在该第三方
		try:
			client = current_app.miniorm(ClientModel).get(client_id=params['client_id'])[0]
		except Exception as e:
			# 第三方不存在
			return render_template(
				'home/error.html',
				data={
					'http_code':400,
					'error_code':1006,
					'error_message':error_messages[1006],
					'error_detail':"get参数：{}".format(params)
				}
			), 400

		# 返回登录页面
		return render_template(
			'home/login.html',
			data={
				'account':params.get('account',""),
				'password':params.get('password',""),
				'redirect_uri':params.get('redirect_uri'),
				'response_type':params.get('response_type'),
				'client_name':client.client_name,
				'client_id':params.get('client_id'),
				'scope':params.get('scope'),
			}
		), 400

	# 账号密码登录
	elif request.method == 'POST':
		
		# 参数反序列化（后期改进，用flash报错）
		try:
			params = PostSchema().load(request.values)
			logger.debug(params)
		except Exception as e:
			# 参数错误 
			return render_template(
				'home/error.html',
				data={
					'http_code':400,
					'error_code':1007,
					'error_message':error_messages[1007],
					'error_detail':str(e)
				}
			), 400

		try:
			# 用户认证
			try:
				user = current_app.miniorm(UserModel).get(
					account=params.get('account'),
					password=params.get('password'),
				)[0]
			except Exception as e:
				logger.debug(e)
				raise UserNotFound

			# 检查第三方
			try:
				client = current_app.miniorm(ClientModel).get(
					client_id=params.get('client_id'),
				)[0]
			except Exception as e:
				raise ClientNotFound

			# 检查scope
			try:
				want_scope = getattr(Scope,params.get('scope'))
			except Exception as e:
				raise ScopeNotExisted

			# 判断权限
			if not BasePermission.can(
				client.scope,
				want_scope
			):
				raise ScopeNotAllowed

			# 检查response_type，生成code或token
			if params.get('response_type') == ResponseType.code:
				try:
					init_data = {
						'secret_key':current_app.settings.token_secret_key,
						'salt':current_app.settings.token_salt,
						'expire_in':current_app.settings.token_expiration,
					}
					encrypt_data = {
						'client_id':params['client_id'],
						'user_id':user.id,
						'scope':params['scope']
					}
					logger.debug('>>>> issue code params:')
					logger.debug(init_data)
					logger.debug(encrypt_data)
					code = Code(
						**init_data
					).issue(
						**encrypt_data
					)
					redirect_uri = "".join([
						params['redirect_uri'],
						"&" if "?" in params['redirect_uri'] else "?",
						"code=",
						code,
					])
				except Exception as e:
					raise IssueCodeError
			elif params.get('response_type') == ResponseType.token:
				try:
					access_token, \
					refresh_token, \
					access_token_expires_in, \
					refresh_token_expires_in = Token(
						secret_key=current_app.settings.token_secret_key,
						salt=current_app.settings.token_salt,
						expire_in=current_app.settings.token_expiration,
					).issue(
						client_id=params['client_id'],
						user_id=user.id,
						scope=params['scope']
					)
					redirect_uri = "".join([
						params['redirect_uri'],
						"&" if "?" in params['redirect_uri'] else "?",
						"token=",access_token,
						"&","refresh_token=",refresh_token,
						"&","access_token_expires_in=",access_token_expires_in,
						"&","refresh_token_expires_in=",refresh_token_expires_in,
					])
				except Exception as e:
					raise IssueTokenError
			else:
				raise ResponseTypeNotExisted

		except UserNotFound as e:
			logger.debug('>>>> 账号或密码错误!')
			flash('账号或密码错误!','warning')
		except ClientNotFound as e:
			logger.debug('>>>> 第三方应用不存在！!')
			flash('第三方应用不存在！','warning')
		except ScopeNotExisted:
			logger.debug('>>>> 不存在的scope！!')
			flash('不存在的scope！','warning')
		except ScopeNotAllowed as e:
			logger.debug('>>>> 第三方应用没有这个权限！!')
			flash('第三方应用没有这个权限！','warning')
		except ResponseTypeNotExisted:
			logger.debug('>>>> 不存在的response_type！!')
			flash('不存在的response_type！','warning')
		except IssueCodeError as e:
			logger.debug('>>>> 生成code失败！!')
			logger.error(traceback.format_exc())
			flash('生成code失败！','warning')
		except IssueTokenError as e:
			logger.debug('>>>> 生成token失败！!')
			logger.error(traceback.format_exc())
			flash('生成token失败！','warning')

		# 重定向回client服务器
		else:
			return redirect(redirect_uri)

		# 出错，返回登录页面
		return render_template(
			'home/login.html',
			data={
				'account':params.get('account',""),
				'password':params.get('password',""),
				'redirect_uri':params.get('redirect_uri'),
				'response_type':params.get('response_type'),
				'client_name':"",
				'client_id':params.get('client_id'),
				'scope':params.get('scope'),
			}
		), 400


@bp.route('/token', methods=['GET',])
def token():
	logger.debug(request.values)

	# 参数验证
	try:
		params = GetTokenSchema().load(request.values)
	except Exception as e:
		return json.dumps({
			'error_code':1001,
			'error_message':error_messages[1001],
			'error_detail':str(e),
		})

	init_data = {
		'secret_key':current_app.settings.token_secret_key,
		'salt':current_app.settings.token_salt,
		'expire_in':current_app.settings.token_expiration,
	}

	# 验证第三方
	try:
		client = current_app.miniorm(ClientModel).get(
			client_id=params['client_id'],
			client_secret=params['client_secret'])[0]
	except Exception as e:
		return json.dumps({
			'error_code':2001,
			'error_message':error_messages[2001],
			'error_detail':str(e),
		})
	

	# code验证
	data = Code(**init_data).verify(params['code'])

	try:
		user = current_app.miniorm(UserModel).get(id=data['user_id'])[0]
	except Exception as e:
		return json.dumps({
			'error_code':1005,
			'error_message':error_messages[1005],
			'error_detail':str(e),
		})

	encrypt_data = {
		'client_id':data['client_id'],
		'user_id':user.id,
		'scope':data['scope']
	}

	# code方式登录
	if params['grant_type'] == GrantType.authorization_code:
		access_token, \
		refresh_token, \
		access_token_expires_in, \
		refresh_token_expires_in = Token(**init_data).issue(**encrypt_data)
		return json.dumps({
			'error_code':0,
			"access_token":access_token,
			"refresh_token":refresh_token,
			"access_token_expires_in":access_token_expires_in,
			"refresh_token_expires_in":refresh_token_expires_in,
		})
	# 其他登录方式
	elif params['grant_type'] in [
		GrantType.implict,
		GrantType.resource_owner_password,
		GrantType.client_credentials,
	]:
		return json.dumps({
			'error_code':1003,
			'error_message':error_messages[1003],
		})
	else:
		return json.dumps({
			'error_code':1004,
			'error_message':error_messages[1004],
		})


	