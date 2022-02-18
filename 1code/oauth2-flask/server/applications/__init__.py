# 第三方库
import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_admin import Admin

db = SQLAlchemy()

#自己的库
from libs.web_utils.miniorm.database.FlaskSqlalchemy import MiniOrm
from .authorization.utils.settings import Settings

# 业务代码
from etc import config

from applications.authorization import Authorization
from applications.resource import Resource
from .authorization.models import (
	Configuration as ConfigurationModel,
)


# 实例化
authoirzation = Authorization()
resource = Resource()
bootstrap = Bootstrap()

miniorm = MiniOrm(db)
settings = Settings(
	miniorm=miniorm,
	settings_cls=ConfigurationModel,
)

def create_app(config_name='default',server_name=__name__):

	app = Flask(server_name)

	# 配置
	app.config.from_object(config[config_name])
	app_context = app.app_context()
	app_context.push()

	# 模板路径
	template_path = os.path.abspath(
		os.path.join(
				os.path.dirname(__file__)
			,
			"../",
			'templates',
		)
	)
	bp = Blueprint('tempalte',__name__,template_folder=template_path)
	app.register_blueprint(bp)

	# 初始化
	db.init_app(app)
	app.db = db

	# admin
	admin = Admin(
		app,
		name="统一登录系统",
		template_mode="bootstrap3",
		url="/{}/admin".format(app.config['PROJECT_NAME'])
	)

	authoirzation.init_app(app,admin,db)
	resource.init_app(app)

	bootstrap.init_app(app)

	

	# 单例
	app.settings = settings
	app.miniorm = miniorm

	# # db.drop_all()
	# db.create_all()
	# db.session.commit()

	app_context.pop()

	return app