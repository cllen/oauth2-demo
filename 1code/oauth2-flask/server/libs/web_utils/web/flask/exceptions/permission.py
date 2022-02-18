from .base import BaseHTTPException

class PermissionException(BaseHTTPException):

    category = 'web-utils'

    co_msg_mapping = {
        109899: {
            'message': 'perimission is not allowed!',
            'http_code': 400,
            'sub_category': 'permission'
        },
        109898: {
            'message': '<request object> has no attribute "user"',
            'http_code': 400,
            'sub_category': 'permission'
        },
    }