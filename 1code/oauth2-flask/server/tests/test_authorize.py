import re
import unittest
import json

from pprint import pprint

from applications import create_app

from etc import TestingConfig

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

class AuthorizeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing','testing')
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
        # register a new account
        response = self.client.post('/oauth2/authorization/authorize', data={
            'account': TestingConfig.testing_user_account,
            'password': TestingConfig.testing_user_password,

            'response_type': ResponseType.code,
            'client_id': TestingConfig.testing_client_id,
            'redirect_uri': 'localhost:5000/{}/code_callback'.format(TestingConfig.PROJECT_NAME),
            'scope': 'snsapi_base',
        })
        self.assertEqual(response.status_code, 302)

        self.assertTrue(re.search('code',
                                  response.get_data(as_text=True)))

        args = get_url_args(response.location)

        href = Href('/oauth2/authorization/token')
        url = href(
            grant_type='authorization_code',
            client_id=TestingConfig.testing_client_id,
            client_secret=TestingConfig.testing_client_secret,
            code=args['code']
        )

        response = self.client.get(url)

        json_response = json.loads(response.get_data(as_text=True))

        # print(json_response)

        self.assertEqual(json_response['error_code'], 0)
        self.assertIsNotNone(json_response.get('access_token'))

        # 获取用户信息
        href = Href('/oauth2/resource/api/v1/user')
        url = href(
            client_id=TestingConfig.testing_client_id,
            client_secret=TestingConfig.testing_client_secret,
            user_access_token=json_response.get('access_token'),
        )

        response = self.client.get(url)

        # print('>>>> test')
        # print(url)
        # pprint(response.get_data(as_text=True))

        json_response = json.loads(response.get_data(as_text=True))

        # print(json_response)

        self.assertEqual(response.status_code,200)
        self.assertEqual(json_response.get('error_code'),0)
        self.assertIsNotNone(json_response.get('entry'))
        self.assertEqual(json_response.get('entry').get('username'), TestingConfig.testing_user_name)

        print('>>> 获取用户信息成功 <<<')


        # self.assertTrue(re.search('陈锡',
        #                           response.get_data(as_text=True)))

        # self.assertTrue(
        #     'You have not confirmed your account yet' in response.get_data(
        #         as_text=True))

