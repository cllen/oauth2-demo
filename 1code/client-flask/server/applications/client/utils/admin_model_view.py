from flask_admin.contrib import sqla

class ModelView(sqla.ModelView):

	def get_query(self):
		self.session.flush()
		self.session.commit()
		return super().get_query()
