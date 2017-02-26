import json

class CustomerRegistry(object):
	"""
		Central cab register
	"""
	def __init__(self):
		self.__registry = dict()

	def register_customer(self, customer_obj):
		_id = customer_obj.get_customer_id()
		self.__registry[_id] = customer_obj

	def get_customer_info(self, customer_id):
		if customer_id not in self.__registry:
			raise ValueError("Customer information not found !!!")

		return self.__registry[customer_id]

	# def get_all_registered_customers(self):
	# 	for cust_id, cust_obj in self.__registry.items():
	# 		print cust_id, cust_obj.to_dict()