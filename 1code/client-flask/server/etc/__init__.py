import os
import abc
import socket

class SystemConfigurations:

	"""
		这里的配置是给开发者修改的。

		存放了如文件路径等参数。
	"""

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

class DevConfiguration(SystemConfigurations):

	"""
		这里的配置是给运维修改的。

		存放了：数据库、管理后台账号密码等参数。
	"""

	# applications
	SECRET_KEY = 'RSAFHJDASKFGHJLASKJ'
	
	# sqlalchemy
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	# admin
	FLASK_ADMIN_USERNAME = 'admin'
	FLASK_ADMIN_PASSWORD = 'admin'

	DOMAIN = 'http://127.0.0.1:5000'


class Configuration(DevConfiguration):

	PROJECT_NAME = 'client' # authorization and resource

	# sqlalchemy
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
		user='xxx', 
		password='xxx', 
		server='ip:port',
		database='client')
