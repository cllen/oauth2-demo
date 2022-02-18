from .apis.v1 import bp as bp_resource

class Resource:

	def __init__(self,app=None):
		if None not in [app,]:
			self.init_app(app)

	def init_app(self,app):
		app.resource = self

		# 接口
		app.register_blueprint(
			bp_resource, 
			url_prefix='/{}/resource/api/v1'.format(
				app.config['PROJECT_NAME'],
			)
		)