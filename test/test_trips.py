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

class TripsTest(unittest.TestCase):
	def setUp(self):
		self.__cab_registry = CabRegistry()
		self.__customer_registry = CustomerRegistry()
		self.__trip_registry = TripRegistry()
		self.__cab_dispatcher = CabDispatcher(self.__cab_registry)
		self.__trip_dispatcher = TripDispatcher(self.__cab_dispatcher, self.__trip_registry)

	def test_trip_start_with_invalid_trip_id(self):
		"""
			Tests if with invalid details, trip can be started.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		trip_started_response = json.loads(customer_action.board_cab('123-hfje33-3344'))

		self.assertFalse(trip_started_response["is_success"])
		self.assertEqual(trip_started_response["response_code"], 250)
		self.assertEqual(trip_started_response["error_message"], "Trip information not found !!!")

	def test_trip_finished_without_trip_start(self):
		"""
			Tests if trip can be finished without starting it.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		response_for_finished_trip = json.loads(customer_action.make_payment_and_offboard(response_for_cab_request["data"]["trip_id"]))

		self.assertFalse(response_for_finished_trip["is_success"])
		self.assertEqual(response_for_finished_trip["response_code"], 250)
		self.assertEqual(response_for_finished_trip["error_message"], "Trip not started")

	def test_trip_order_amount(self):
		"""
			Checks order amount generation after trip gets completed.
			Order amount is that amount which customer ows after completing the trip.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.CabColor.COLOR_PINK
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location, color))
		trip_started_response = json.loads(customer_action.board_cab(response_for_cab_request["data"]["trip_id"]))
		response_for_finished_trip = json.loads(customer_action.make_payment_and_offboard(response_for_cab_request["data"]["trip_id"]))

		self.assertTrue(response_for_finished_trip["is_success"])
		self.assertEqual(response_for_finished_trip["response_code"], 200)
		self.assertEqual(response_for_finished_trip["data"]["order_summary"]["order_amount"], 238.35)