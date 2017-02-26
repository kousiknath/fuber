import sys
from src.fuber_core import utils
import datetime
from src.registry import trip_status
import copy
from src.response import standard_response
from src.response.standard_response import ApplicationErrorCodes
from src.models.order import Order

class Trip(object):
	def __init__(self, trip_request, cab_action, trip_registry, *args, **kwargs):
		self.__request = trip_request
		self.__cab_action = cab_action
		self.__order = None

		self.__trip_id = utils.get_id()
		self.__trip_start_time = None
		self.__trip_end_time = None
		self.__trip_duration = None
		self.__trip_status = trip_status.TRIP_DISPATCHED # Initial stage of the trip
		self.__trip_allocation_time = datetime.datetime.now()
		self.__trip_distance = 0.0 # Assumed to be in Kilometers

		self.__args = args
		self.__kwargs = kwargs

		trip_registry.register_trip(self)

	def get_trip_id(self):
		return self.__trip_id

	def start_trip(self):
		if self.__trip_status != trip_status.TRIP_DISPATCHED:
			return standard_response.get_standard_api_response(False, "Trip not requested / dispatched", ApplicationErrorCodes.REQUEST_NOT_FULFILLED)

		self.__trip_start_time = datetime.datetime.now()
		self.__trip_status = trip_status.TRIP_STARTED

		return standard_response.get_standard_api_response(True, "", ApplicationErrorCodes.SUCCESS, self.to_dict())

	def cancel_trip(self):
		if not self.__is_trip_cancellable():
			return standard_response.get_standard_api_response(False, "Trip not requested, not dispatched or already started", ApplicationErrorCodes.REQUEST_NOT_FULFILLED)

		self.__trip_status = trip_status.TRIP_CANCELLED
		self.__cab_action.deallocate_cab()

		return standard_response.get_standard_api_response(True, "", ApplicationErrorCodes.SUCCESS, self.to_dict())

	def __is_trip_cancellable(self):
		if self.__trip_status == trip_status.TRIP_DISPATCHED:
			return True

		return False

	def end_trip(self):
		if self.__trip_status != trip_status.TRIP_STARTED:
			return standard_response.get_standard_api_response(False, "Trip not started", ApplicationErrorCodes.REQUEST_NOT_FULFILLED)

		self.__trip_status = trip_status.TRIP_COMPLETED		
		self.__cab_action.deallocate_cab()
		self.__cab_action.update_cab_location(self.__request.get_trip_end_location())
		self.__trip_distance = utils.get_trip_distance(self.__request.get_trip_start_location(), self.__request.get_trip_end_location())
		self.__trip_duration = utils.get_trip_timing(self.__trip_distance)  # self.__trip_end_time - self.__trip_start_time
		self.__trip_end_time = self.__trip_start_time + datetime.timedelta(minutes = int(self.__trip_duration)) # datetime.now()
		self.__order = Order(self.__trip_id, self.__request.get_trip_customer(), self.__trip_distance, self.__trip_duration, self.__request.get_trip_preference().get_cab_color())

		return standard_response.get_standard_api_response(True, "", ApplicationErrorCodes.SUCCESS, self.to_dict())

	def generate_order_details(self):
		pass

	def to_dict(self):
		order_summary = {}

		if self.__order is not None:
			order_summary = self.__order.to_dict()

		return {"trip_request" : self.__request.to_dict(), "trip_id" : str(self.__trip_id), "trip_start_time" : str(self.__trip_start_time), "trip_end_time" : str(self.__trip_end_time), "trip_duration" : str(self.__trip_duration), "trip_status" : trip_status.get_trip_status(self.__trip_status), "trip_allocation_time: " : repr(self.__trip_allocation_time), "trip_distance" : str(self.__trip_distance), "cab_info" : self.__cab_action.get_cab_info(), "order_summary" : order_summary}

	def get_standard_trip_response(self):
		return standard_response.get_standard_api_response(True, "", ApplicationErrorCodes.SUCCESS, self.to_dict())
