from functools import wraps
from flask import request
from ...permission.base import BasePermission
from .exceptions.permission import PermissionException

def permission(
	requireds=[]
):

	def wrapper1(func):

		@wraps(func)
		def wrapper2(*args, **kwargs):

			func1 = func

			if hasattr(request,'user'):
				user_permission = request.user.permissions
				for required in requireds:
					if not BasePermission.can(
						user_permission=user_permission,
						required_permission=required
					):
						raise PermissionException(109899)
			else:
				raise PermissionException(109898)

			return func1(*args, **kwargs)

		return wrapper2
	return wrapper1
