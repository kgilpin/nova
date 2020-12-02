
class APIException(Exception):
	pass

class LoginException(APIException):
	pass

class ObjectNotFoundException(APIException):
	pass
