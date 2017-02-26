import sys 

class Customer(object):
	def __init__(self, customer_id, customer_name, customer_email, customer_registry):
		self.__customer_id = customer_id
		self.__customer_name = customer_name
		self.__customer_email = customer_email

		customer_registry.register_customer(self)

	def get_customer_id(self):
		return self.__customer_id

	def get_customer_name(self):
		return self.__customer_name

	def to_dict(self):
		return {"id" : str(self.__customer_id), "name" : str(self.__customer_name), "email" : str(self.__customer_email)}