# 第三方库
import os
from flask import Flask, Blueprint 
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin 
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

db = SQLAlchemy()

# 自己的库
from libs.web_utils.miniorm.database.FlaskSqlalchemy import MiniOrm
from .client.utils.settings import Settings

# 业务代码
from .client import Client

from applications.client.admins import (
	Configuration as ConfigurationAdmin,
	User as UserAdmin,
)
from applications.client.models import (
	Configuration as ConfigurationModel,
	User as UserModel,
)

# 实例化
client = Client()

bootstrap = Bootstrap()
bp = Blueprint('views',__name__)
migrate = Migrate()

miniorm = MiniOrm(db)
settings = Settings(
	miniorm=miniorm,
	settings_cls=ConfigurationModel,
)

def create_app(Configuration,import_name=__name__,is_create_all=False):

	"""
		app
	"""
	app = Flask(
		import_name,
		static_url_path='/cms/static',
		static_folder='../static',
		template_folder='../templates'
	)

	"""
		config
	"""
	app.config.from_object(Configuration)
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
	bp_template = Blueprint('template',__name__,template_folder=template_path)
	app.register_blueprint(bp_template)

	"""
		init
	"""

	# database
	db.init_app(app)
	if is_create_all:
		# db.drop_all()
		db.create_all()
		db.session.commit()
	@app.teardown_appcontext
	def shutdown_session(exception=None):
		db.session.remove()
	migrate.init_app(app,db)

	# flask-admin
	admin = Admin(
		app,
		name='第三方应用',
		template_mode='bootstrap3',
		url='/{}/admin'.format(app.config['PROJECT_NAME'])
	)

	# 其他
	bootstrap.init_app(app)

	
	"""
		applications
	"""
	client.init_app(app,admin,db)

	"""
		views
	"""
	app.register_blueprint(
		bp,
		url_prefix='/{}'.format(
			app.config['PROJECT_NAME'],
		)
	)

	app.miniorm = miniorm
	app.settings = settings

	return app
