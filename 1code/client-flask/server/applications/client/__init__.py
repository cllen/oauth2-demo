# 第三方库
from flask import Blueprint
import os
from flask_moment import Moment
from flask_pagedown import PageDown

# 自己的库
from libs.web_utils.settings import BaseSettings

# 业务代码
from .admins import (
	Configuration as ConfigurationAdmin,
	User as UserAdmin,
)
from .models import (
	Configuration as ConfigurationModel,
	User as UserModel,
)

# 实例化
moment = Moment()
pagedown = PageDown()

class Client:

	def __init__(self,app=None,admin=None,db=None):

		if None not in [app,admin,db]:
			self.init_app(app,admin)

	def init_app(self,app,admin,db):
		self.app = app
		self.admin = admin
		app.client = self

		# admin
		admin.add_view(ConfigurationAdmin(name='设置',category="系统数据"))
		admin.add_view(UserAdmin(UserModel, db.session, name=u'用户',category="系统数据"))

		# 初始化第三方插件
		moment.init_app(app)
		pagedown.init_app(app)

		# 视图
		from .views import login
