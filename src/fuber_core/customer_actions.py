import sys
from src.models.trip_request import TripRequest
from src.fuber_core.trip_dispatcher import TripDispatcher
from src.registry import cab_colors
from src.fuber_core import utils
from src.models.trip_preference import TripPreference
import json

class CustomerAction(object):
	"""
		Basic life cycle methods of a customer during a trip.
		The class simulates some basic operation a customer can perform during cab booking.
	"""
	@staticmethod
	def get_action_object(customer_id, trip_dispatcher):
		return CustomerAction(customer_id, trip_dispatcher)

	def __init__(self, customer_id, trip_dispatcher, *args, **kwargs):
		self.__customer_id = customer_id
		self.__trip_dispatcher = trip_dispatcher
		self.__args = args
		self.__kwargs = kwargs

	def request_cab(self, start_location, end_location, cab_color=None, *args, **kwargs):
		"""
			It will generate a trip request which will be delivered to Trip Dispatcher.
			Trip dispatcher in turn will query cab dispatcher to get available cabs if any.
			If any nearest cab is available, a corresponsing Trip wrapped with the cab info will be provided to the customer action. 
		"""
		trip_preference = TripPreference()
		trip_preference.set_cab_color(cab_color)

		trip_request = TripRequest(self.__customer_id, start_location, end_location, trip_preference)
		dispatched_trip_data = self.__trip_dispatcher.process_trip_request(trip_request, *args, **kwargs)
		return dispatched_trip_data

	def board_cab(self, trip_id, *args, **kwargs):
		"""
			This will trigger trip start.
		"""
		started_trip_data = self.__trip_dispatcher.start_trip(trip_id, args, kwargs)
		return started_trip_data

	def make_payment_and_offboard(self, trip_id, *args, **kwargs):
		"""
			This will trigger end trip & order details generation.
		"""
		finished_trip_data = self.__trip_dispatcher.end_trip(trip_id, args, kwargs)
		return finished_trip_data

	def cancel_trip(self, trip_id, *args, **kwargs):
		cancelled_trip_data = self.__trip_dispatcher.cancel_trip(trip_id, args, kwargs)
		return cancelled_trip_data