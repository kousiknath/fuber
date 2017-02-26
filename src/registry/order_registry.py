class OrderRegistry(object):
	"""
		TODO: Central order register.
	"""
	def __init__(self):
		self.__registry = dict()
		self.__registry_by_trip = dict()

	def register_order(self, trip_id, order_obj):
		_id = order_obj.get_customer_id()
		self.__registry[_id] = order_obj
		self.__registry_by_trip[trip_id] = _id

	def get_order_info(self, order_id):
		if order_id not in self.__registry:
			raise ValueError("Customer information not found !!!")

		return self.__registry[order_id]