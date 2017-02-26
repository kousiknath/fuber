import sys
from src.fuber_core import utils
from datetime import datetime

class TripRequest(object):
	def __init__(self, customer_id, trip_start_location, trip_end_location, trip_preference, *args, **kwargs):
		self.__trip_request_id = utils.get_id()
		self.__customer_id = customer_id
		self.__start_location = trip_start_location
		self.__end_location = trip_end_location
		self.__request_time = datetime.now()
		self.__preference = trip_preference

		self.args = args
		self.kwargs = kwargs

	def get_trip_customer(self):
		return self.__customer_id

	def get_trip_start_location(self):
		return self.__start_location

	def get_trip_end_location(self):
		return self.__end_location

	def get_trip_preference(self):
		return self.__preference

	def to_dict(self):
		return {"trip_request_id" : str(self.__trip_request_id), "customer_id" : str(self.__customer_id), "trip_start_location" : self.__start_location.to_dict(), "trip_end_location" : self.__end_location.to_dict(), "trip_requested_time" : repr(self.__request_time), "trip_preference" : self.__preference.to_dict()}