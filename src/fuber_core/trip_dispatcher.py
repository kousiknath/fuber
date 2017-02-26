import sys
from src.models.trip import Trip
import json
from src.response import standard_response
from src.response.standard_response import ApplicationErrorCodes

class TripDispatcher(object):
	def __init__(self, cab_dispatcher, trip_registry, *args, **kwargs):
		self.__cab_dispatcher = cab_dispatcher
		self.__trip_registry = trip_registry
		self.__args = args
		self.__kwargs = kwargs

	def process_trip_request(self, trip_request, *args, **kwargs):
		try:
			allocated_cab_action_obj = self.__cab_dispatcher.allocate_cab_if_available(trip_request.get_trip_start_location(), trip_request.get_trip_preference())
		except Exception as e:
			return standard_response.get_standard_api_response(False, str(e), ApplicationErrorCodes.REQUEST_NOT_FULFILLED)

		trip_data = Trip(trip_request, allocated_cab_action_obj, self.__trip_registry)

		return trip_data.get_standard_trip_response()

	def start_trip(self, trip_id, *args, **kwargs):
		try:
			trip = self.__trip_registry.get_trip_info(trip_id)
		except Exception as e:
			return standard_response.get_standard_api_response(False, str(e), ApplicationErrorCodes.REQUEST_NOT_FULFILLED)
		
		trip_data = trip.start_trip()

		return trip_data

	def end_trip(self, trip_id, *args, **kwargs):
		trip = self.__trip_registry.get_trip_info(trip_id)
		trip_data = trip.end_trip()

		return trip_data	

	def cancel_trip(self, trip_id, *args, **kwargs):
		trip = self.__trip_registry.get_trip_info(trip_id)
		trip_data = trip.cancel_trip()

		return trip_data