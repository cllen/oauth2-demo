# 第三方
from flask import render_template, flash, current_app, request, session, redirect
import requests
import traceback

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 自己的库
from libs.oauth2.client.constants import Scope

from libs.oauth2.utils.constants import GrantType

from libs.oauth2.client.urls import Urls

# 业务代码
from applications import bp
from ..schemas.parsers.login import (
	CodeCallback as CodeCallbackSchema,
	GetToken as GetTokenSchema,
	GetUserinfo as GetUserinfoSchema,
)
from ..models import (
	User as UserModel,
)

from exceptions import error_messages

@bp.route('/home',methods=('GET',))
def home():
	data = session.get('user',{})
	return render_template('home/home.html', data=data)

@bp.route('/login',methods=('GET',))
def login():

	# 生成一个获取用户信息权限的code的url
	redirect_uri = Urls.authorization_code(
		authorization_code_api=current_app.settings.authorization_code_api,
		client_id=current_app.settings.client_id,
		code_callback_api=current_app.settings.client_code2token_api,
		scope=Scope.snsapi_base,
	)

	# 将 referrer 拼接到 redirect_uri
	session['state'] = request.referrer
	return redirect(redirect_uri)

@bp.route('/logout',methods=('GET',))
def logout():
	session['user'] = {}
	return redirect('/client/home')

@bp.route('/code_callback', methods=['GET',])
def code_callback():
	
	# 校验参数
	try:
		params = CodeCallbackSchema().load(request.values)
	except Exception as e: 
		return render_template(
			'home/error.html',
			data={
				'http_code':400,
				'error_code':1001,
				'error_message':error_messages[1001],
				'error_detail':traceback.format_exc(),
				'error_html':None,
			}
		), 400


	# 获取token
	url = Urls.get_token(
		token_api=current_app.settings.code2token_api,
		client_id=current_app.settings.client_id,
		client_secret=current_app.settings.client_secret,
		grant_type=GrantType.authorization_code,
		code=params['code']
	)
	resp = requests.get(url)
	
	logger.debug('>>>> get,token:')
	logger.debug(url)
	# logger.debug(resp.text)
	# logger.debug(resp.json())


	# 校验统一登录系统返回的参数，是否为json类型
	try:
		assert resp.status_code == 200
		# assert resp.headers['Content-Type'] == 'application/json'
	except Exception as e:
		# 统一登录系统返回错误网页 
		return render_template(
			'home/error.html',
			data={
				'http_code':500,
				'error_code':1003,
				'error_message':error_messages[1003],
				'error_detail':traceback.format_exc(),
				'error_html':resp.text,
			}
		), 500

	# 反序列化返回的json数据
	try:
		params = GetTokenSchema().loads(resp.text)
	except Exception as e:
		# 统一登录系统返回不可识别json参数 
		return render_template(
			'home/error.html',
			data={
				'http_code':500,
				'error_code':1004,
				'error_message':error_messages[1004],
				'error_detail':traceback.format_exc(),
				'error_html':resp.text,
			}
		), 500

	# 获取用户信息
	url = Urls.get_userinfo(
		userinfo_api=current_app.settings.token2userinfo_api,
		client_id=current_app.settings.client_id,
		client_secret=current_app.settings.client_secret,
		user_access_token=params['access_token']
	)
	resp = requests.get(url)
	
	# 校验统一登录系统返回的参数，是否为json类型
	try:
		assert resp.status_code == 200
		#assert resp.headers['Content-Type'] == 'application/json'
	except Exception as e:
		# 统一登录系统返回不可识别json参数 
		return render_template(
			'home/error.html',
			data={
				'http_code':500,
				'error_code':1005,
				'error_message':error_messages[1005],
				'error_detail':traceback.format_exc(),
				'error_html':resp.text,
			}
		), 500


	# 反序列化返回的json数据
	try:
		logger.debug('>>>> get,userinfo:')
		logger.debug(resp.json())
		params = GetUserinfoSchema().loads(resp.text)
	except Exception as e:
		# 统一登录系统返回不可识别json参数 
		return render_template(
			'home/error.html',
			data={
				'http_code':500,
				'error_code':1007,
				'error_message':error_messages[1007],
				'error_detail':traceback.format_exc(),
				'error_detail2':resp.text,
			}
		), 500

	# 校验返回的参数
	try:
		assert params['error_code'] == 0
	except Exception as e: 
		return render_template(
			'home/error.html',
			data={
				'http_code':500,
				'error_code':1008,
				'error_message':error_messages[1008],
				'error_detail':params,
			}
		), 500

	logger.debug('>>>> get,userinfo:')
	logger.debug(url)
	logger.debug(params)

	"""
		业务代码部分
	"""
	# 进行用户登录或注册
	userinfo = params['entry']
	# 查询或存储用户
	user = None
	try:
		user = current_app.settings.miniorm(UserModel).get(oauth2_user_id=userinfo['id'])[0]
	except:
		logger.debug('>>>> user not found,creating:')
	if not user:
		user = current_app.settings.miniorm(UserModel).save(
			id=userinfo['id'],
			oauth2_user_id=userinfo['id'],
			account=userinfo['account'],
			username=userinfo['username'],
			type=userinfo['type'],
		)
		user = current_app.settings.miniorm(UserModel).get(oauth2_user_id=userinfo['id'])[0]
	# 记录登录状态方案： session / token，这里选择session
	session['user'] = {'oauth2_user_id':user.oauth2_user_id,'username':userinfo['username']}
	state = session.get('referrer') or current_app.settings.client_default_uri
	# 重定向回锚点
	return redirect(state)