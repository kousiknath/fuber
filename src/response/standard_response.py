import json

"""
	Error Code Convention:
	1. Successful response: 200
	2. Request Accepted but could n't be processed: 250 (assumed)
	3. Internal Server Error: 500
"""
class ApplicationErrorCodes(object):
	SUCCESS = 200
	REQUEST_NOT_FULFILLED = 250
	INTERNAL_SERVER_ERROR = 500

class StandardResponse(object):
	def __init__(self, is_success, error, code, data={}):
		self.__response = {"is_success" : is_success, "error_message" : error, "response_code" : code, "data" : data or {}}

	def to_string(self):
		return json.dumps(self.__response)


def get_standard_api_response(status, error, code, data={}):
	response = StandardResponse(status, error, code, data)
	return response.to_string()