error_messages = {
	1001:"参数错误！",
	1002:"未知错误！",
	1003:"授权方式不支持！",
	1004:"授权方式不存在！",
	1005:"用户不存在！",
	1006:"第三方不存在！",
	1007:"账号密码登录时候反序列化参数错误！",

	2001:"第三方账号密码错误！",
	2002:"token缺少参数！",
	2003:"该token不属于当前第三方！",
	2004:"token里的scope值无效！",
	2005:"token里的用户不存在！",

}

from .authorize import (
	UserNotFound,
	ClientNotFound,
	ScopeNotExisted,
	ScopeNotAllowed,
	IssueCodeError,
	IssueTokenError,
	ResponseTypeNotExisted,
)
