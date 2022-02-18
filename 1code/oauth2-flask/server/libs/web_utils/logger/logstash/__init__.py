from .get_logger import get_logstash_logger

logstash_data = {
	
	'@timestamp':"",
	'@version':"",

	'http_code':0,
	'error_code':0,
	'error_message':"",
	'error_traceback':"",

	'http_authorization':"",
	'api_name':"",
	'api_url':"",
	'arguments':"",

	'user_openid':"",
	'user_nickname':"",
}