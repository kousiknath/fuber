import unittest
import decimal
import random
import json

from src.fuber_core.customer_actions import CustomerAction
from src.models.location import Location
from src.registry.cab_registry import CabRegistry
from src.registry.customer_registry import CustomerRegistry
from src.registry.trip_registry import TripRegistry
from src.fuber_core.cab_dispatcher import CabDispatcher
from src.fuber_core.trip_dispatcher import TripDispatcher
from src.registry import cab_colors
from src.models.cab import Cab, ColoredCab

class TestCabDispatch(unittest.TestCase):
	def setUp(self):
		self.__cab_registry = CabRegistry()
		self.__customer_registry = CustomerRegistry()
		self.__trip_registry = TripRegistry()
		self.__cab_dispatcher = CabDispatcher(self.__cab_registry)
		self.__trip_dispatcher = TripDispatcher(self.__cab_dispatcher, self.__trip_registry)

	def test_dispatch_without_cab(self):
		"""
			Without cabs being registered, no cab can be allocated on customer's request.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		"""
			No cab has been registered here. So no cab available. Customer request will be rejected.
		"""

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))

		self.assertFalse(response_for_cab_request["is_success"])
		self.assertEqual(response_for_cab_request["response_code"], 250)
		self.assertEqual(response_for_cab_request["error_message"], "No cab can be allocated")

	def test_dispatch_with_cab_color(self):
		"""
			Tests if cabs with a specific color can be dispatched on customer's request.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		"""
			PINK color is assigned to the cab.
		"""
		color = cab_colors.CabColor.COLOR_PINK
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location, color))

		self.assertEqual(response_for_cab_request["response_code"], 200)
		self.assertEqual(response_for_cab_request["error_message"], "")
		self.assertEqual(response_for_cab_request["data"]["cab_info"]["color"], "Pink")

	def test_dispatch_without_specific_cab_color(self):
		"""
			Tests if cabs without any specific color request can be dispatched.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))

		self.assertEqual(response_for_cab_request["response_code"], 200)
		self.assertEqual(response_for_cab_request["error_message"], "")
		self.assertEqual(response_for_cab_request["data"]["cab_info"]["color"], "White(Default)")