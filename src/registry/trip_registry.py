import sys
import json

class TripRegistry(object):
	"""
		Central cab register
	"""
	def __init__(self):
		self.__registry = dict()

	def register_trip(self, trip_obj):
		_id = trip_obj.get_trip_id()
		self.__registry[_id] = trip_obj

	def get_trip_info(self, trip_id):
		if trip_id not in self.__registry:
			raise ValueError("Trip information not found !!!")

		return self.__registry[trip_id]

	def get_all_registered_trips(self):
		for trip_id, trip_obj in self.__registry.items():
			print trip_id, trip_obj.to_string()