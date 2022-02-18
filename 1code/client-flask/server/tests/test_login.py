import re
import unittest
import json

from applications import create_app
from etc import Configuration

from libs.oauth2.utils.constants import (
	Scope,
	ResponseType,
	GrantType
)

from werkzeug.urls import url_parse,Href

def get_url_args(url):
    parser = url_parse(url)
    args = parser.query.split('&')
    args = {arg.split('=')[0]:arg.split('=')[1] for arg in args}
    return args

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Configuration,'testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()
        # Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_login(self):
        pass