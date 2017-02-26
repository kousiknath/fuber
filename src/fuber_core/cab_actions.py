import sys
from src.models.cab import Cab

class CabAction(object):
	"""
		Basic life cycle methods of a cab during a trip
	"""
	def __init__(self, cab):
		self.__cab = cab

	def allocate_cab(self):
		"""
			Reserve the cab so that it becomes unavailable for other customer.
		"""
		if self.__cab is None:
			raise ValueError("No cab can be allocated")

		self.__cab.allocate()

	def deallocate_cab(self):
		"""
			Deallocate the cab after trip is complete or cancelled.
		"""
		if self.__cab is None:
			raise ValueError("No cab can be deallocated")

		self.__cab.deallocate()

	def update_cab_location(self, new_location):
		if self.__cab is None:
			raise ValueError("No updation operation can be run on None type object")

		self.__cab.update_location(new_location)

	def get_cab_info(self):
		if self.__cab is None:
			raise ValueError("No cab info can be fetched")

		return self.__cab.to_dict()