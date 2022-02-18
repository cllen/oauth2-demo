import os
import abc
import socket

class SystemConfig:

	"""
		这里的配置是给开发者修改的。

		存放了如文件路径等参数。
	"""

	# applications
	SECRET_KEY = 'RSAFHJDASKFGHJLASKJ'

	# sqlalchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	# flask-admin-image,video,file
	UPLOADS_PATH = os.path.join(
		os.path.abspath(os.getcwd()), 
		"static",
		"uploads"
	)

	def get_FILE_UPLOAD_URL(self):
		return "".join([
			self.DOMAIN,
			"/",
			self.PROJECT_NAME,
			"/",
			"static",
			"/"
			"uploads",
			"/"
		])

	def get_FILE_DOWNLOAD_URL(self):
		return self.get_FILE_UPLOAD_URL()


class Config(SystemConfig):

	# flask-admin
	FLASK_ADMIN_USERNAME = 'admin'
	FLASK_ADMIN_PASSWORD = 'admin'

	DOMAIN = 'http://127.0.0.1:5000'

	PROJECT_NAME = 'oauth2' # authorization and resource

	# sqlalchemy
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
		user='xxx', 
		password='xxx', 
		server='ip:port',
		database='oauth2')

class TestingConfig(SystemConfig):

	PROJECT_NAME = 'oauth2' # authorization and resource

	DOMAIN = 'http://127.0.0.1:5000'

	# flask-admin
	FLASK_ADMIN_USERNAME = 'admin'
	FLASK_ADMIN_PASSWORD = 'admin'

	testing_client_id = '1'
	testing_client_secret = 'xxx'
	testing_client_name = 'test-client'
	testing_client_scope = 1

	testing_user_account = '20203712062'
	testing_user_password = '123'
	testing_user_name = '陈锡'
	testing_user_type = '学生'

	# sqlalchemy
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'server-testing.sqlite')


class ProductionConfig(SystemConfig):

	PROJECT_NAME = 'oauth2' # authorization and resource

	# flask-admin
	FLASK_ADMIN_USERNAME = 'admin'
	FLASK_ADMIN_PASSWORD = 'admin'	

	DOMAIN = 'http://127.0.0.1:5000'

	# sqlalchemy
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
		user='xxx', 
		password='xxx', 
		server='ip:port',
		database='oauth2')

config = {
	# 'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	# 'heroku': HerokuConfig,
	# 'docker': DockerConfig,
	# 'unix': UnixConfig,

	'default': ProductionConfig
}