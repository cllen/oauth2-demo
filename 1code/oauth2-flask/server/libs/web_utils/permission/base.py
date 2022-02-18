class BasePermission:

	@staticmethod
	def can(user_permission,required_permission):
		return (user_permission & required_permission == required_permission)

	@staticmethod
	def add(current_permission,additional_permission):
		return current_permission | additional_permission
