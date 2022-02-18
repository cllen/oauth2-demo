from .base import BaseHTTPException

class AuthorizationException(BaseHTTPException):
    # category
    # auth: 98
    category = 'web-utils'

    # application : apis : number
    # 10:none
        # 99:authorization
        # 98:throttling
        # 97:permission
    # 11 wechat
    co_msg_mapping = {
        109999: {
            'message': 'missing authorization field!',
            'http_code': 400,
            'sub_category': 'authorization'
        },
        109998: {
            'message': 'authorization type not found!',
            'http_code': 400,
            'sub_category': 'authorization'
        },
    }