from .views import bp as bp_authorization

from .admins import (
	Configuration as ConfigurationAdmin,
	Client as ClientAdmin,
	User as UserAdmin,
)

from .models import (
	Configuration as ConfigurationModel,
	User as UserModel,
	Client as ClientModel,
)

class Authorization:

	def __init__(self,app=None,admin=None,db=None):
		if None not in [app,admin,db,]:
			self.init_app(app,admin,db)

	def init_app(self,app,admin,db):
		
		app.authorization = self

		# admin
		admin.add_view(ConfigurationAdmin(name=u'设置'))
		admin.add_view(ClientAdmin(ClientModel, db.session, name=u'开发者'))
		admin.add_view(UserAdmin(UserModel, db.session, name=u'用户'))


		# 接口
		app.register_blueprint(
			bp_authorization, 
			url_prefix='/{}/authorization'.format(
				app.config['PROJECT_NAME'],
			)
		)