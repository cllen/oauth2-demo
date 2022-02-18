#coding:utf8
from ._imports_ import *

logger = logging.getLogger(__name__)

# 自己的库
from libs.oauth2.authorization import Token

# 业务代码
from applications.resource.schemas.marshals.user import (
	Get as GetMarshal,
)

from applications.resource.schemas.parsers.user import (
	Get as GetParser,
)

from applications.authorization.models import (
	User as UserModel,
	Client as ClientModel,
)

from exceptions import (
	error_messages
)

@api.route('/user')
class Single(Resource):

	@api.doc(parser=GetParser)
	@api.marshal_with(GetMarshal)
	def get(self):

		try:
			args = GetParser.parse_args()
		except Exception as e:
			return {
				'error_code':1001,
				'error_message':error_messages[1001],
				'error_detail':e,
				'error_detail2':traceback.format_exc(),
			}

		logger.debug('>>>> args:')
		logger.debug(args)

		try:
			client = current_app.miniorm(ClientModel).get(
				client_id=args['client_id'],
				client_secret=args['client_secret'])[0]
		except Exception as e:
			return {
				'error_code':2001,
				'error_message':error_messages[2001],
				'error_detail':e,
			}

		logger.debug('>>>> client:')
		logger.debug(client)

		init_data = {
			'secret_key':current_app.settings.token_secret_key,
			'salt':current_app.settings.token_salt,
			'expire_in':current_app.settings.token_expiration,
		}

		token_data = Token(**init_data).verify(args['user_access_token'])

		logger.debug('>>>> token_data:')
		logger.debug(token_data)

		

		if None in [
			token_data.get('scope'),
			token_data.get('client_id'),
			token_data.get('user_id'),
		]:
			return {
				'error_code':2002,
				'error_message':error_messages[2002],
			}

		if args['client_id'] != token_data['client_id']:
			return {
				'error_code':2003,
				'error_message':error_messages[2003],
			}

		try:
			want_scope = getattr(Scope,token_data.get('scope'))
		except Exception as e:
			return {
				'error_code':2004,
				'error_message':error_messages[2004],
				'error_detail':e,
			}

		try:
			user = current_app.miniorm(UserModel).get(id=token_data['user_id'])[0]
		except Exception as e:
			return {
				'error_code':2005,
				'error_message':error_messages[2005],
				'error_detail':e,
			}

		logger.debug('>>>> user:')
		logger.debug(user.to_dict())
		
		return {
			'error_code':0,
			'entry':user,
		}