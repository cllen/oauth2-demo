from ..utils.admin_model_view import ModelView

class User(ModelView):

	column_labels = {
		'id':'第三方应用的用户id',
		'oauth2_user_id':'统一登录系统的用户id',
		'account':'用户的账号/学号/工号',
		'type':'用户的类型（学生/教师/管理员）',
		'username':'用户的名名字',
	}

	column_list = [
		'id',
		'oauth2_user_id',
		'account',
		'username',
		'type',
	]