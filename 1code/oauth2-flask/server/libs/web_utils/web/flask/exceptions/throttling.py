from .base import BaseHTTPException

class ThrottlingException(BaseHTTPException):

    category = 'web-utils'

    co_msg_mapping = {
        109799: {
            'message': 'Access frequency is limited!',
            'http_code': 400,
            'sub_category': 'throttling'
        },
    }