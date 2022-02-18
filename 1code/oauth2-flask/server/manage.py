import os
import click
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask_migrate import Migrate

from applications import create_app 

migrate = Migrate()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate.init_app(app)

# 初始化测试数据库命令
@app.cli.command('init-testing-database')
def init_testing_database():

	logger.debug('>>> 正在初始化数据库... <<<')

	logger.debug('1/3 正在创建数据库')

	app.db.drop_all()
	app.db.create_all()
	app.db.session.commit()

	from applications.authorization.models import (
		User as UserModel,
		Client as ClientModel,
	)
	from etc import TestingConfiguration

	client_data = {
		'client_id':TestingConfiguration.testing_client_id,
		'client_secret':TestingConfiguration.testing_client_secret,
		'client_name':TestingConfiguration.testing_client_name,
		'scope':TestingConfiguration.testing_client_scope
	}
	user_data = {
		'password':TestingConfiguration.testing_user_password,
		'username':TestingConfiguration.testing_user_name,
		'account':TestingConfiguration.testing_user_account,
		'type':TestingConfiguration.testing_user_type,
	}

	logger.debug('2/3 正在插入第三方数据:',client_data)
	app.miniorm(ClientModel).save(**client_data)

	logger.debug('3/3 正在插入用户数据:',user_data)
	app.miniorm(UserModel).save(**user_data)

	logger.debug('>>> 初始化数据库成功! <<<')


# 运行测试程序命令
@app.cli.command('run-tests')
@click.argument('test_names', nargs=-1)
def run_tests(test_names=None):
	
	COV = None
	# if os.environ.get('FLASK_COVERAGE'):
	import coverage
	COV = coverage.coverage(branch=True, include='./*')
	COV.start()

	import unittest
	if test_names:
		tests = unittest.TestLoader().loadTestsFromNames(test_names)
	else:
		tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

	if COV:
		COV.stop()
		COV.save()
		print('Coverage Summary:')
		COV.report()
		basedir = os.path.abspath(os.path.dirname(__file__))
		covdir = os.path.join(basedir, 'tmp/coverage')
		COV.html_report(directory=covdir)
		print('HTML version: file://%s/index.html' % covdir)
		COV.erase()


if __name__ == '__main__':
	app.run(debug=True,port=5001)


