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


class TripStatusTest(unittest.TestCase):

	def setUp(self):
		self.__cab_registry = CabRegistry()
		self.__customer_registry = CustomerRegistry()
		self.__trip_registry = TripRegistry()
		self.__cab_dispatcher = CabDispatcher(self.__cab_registry)
		self.__trip_dispatcher = TripDispatcher(self.__cab_dispatcher, self.__trip_registry)

	def test_trip_dispatched_status(self):
		"""
			Checks trip allocation / dispatch status.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		self.assertTrue(response_for_cab_request["is_success"])
		self.assertEqual(response_for_cab_request["response_code"], 200)
		self.assertEqual(response_for_cab_request["data"]["trip_status"], "Trip Allocated")

	def test_trip_start_status(self):
		"""
			Checks status of the trips when it starts.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		trip_started_response = json.loads(customer_action.board_cab(response_for_cab_request["data"]["trip_id"]))

		self.assertTrue(trip_started_response["is_success"])
		self.assertEqual(trip_started_response["response_code"], 200)
		self.assertEqual(trip_started_response["data"]["trip_status"], "Trip Started")

	def test_trip_complete_status(self):
		"""
			Checks status of the trip when it gets completed.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		trip_started_response = json.loads(customer_action.board_cab(response_for_cab_request["data"]["trip_id"]))
		response_for_finished_trip = json.loads(customer_action.make_payment_and_offboard(response_for_cab_request["data"]["trip_id"]))

		self.assertTrue(response_for_finished_trip["is_success"])
		self.assertEqual(response_for_finished_trip["response_code"], 200)
		self.assertEqual(response_for_finished_trip["data"]["trip_status"], "Trip Completed")

	def test_trip_cancel_status(self):
		"""
			Checks trip status after customer cancels it.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		trip_cancelled_response = json.loads(customer_action.cancel_trip(response_for_cab_request["data"]["trip_id"]))

		self.assertTrue(trip_cancelled_response["is_success"])
		self.assertEqual(trip_cancelled_response["response_code"], 200)
		self.assertEqual(trip_cancelled_response["data"]["trip_status"], "Trip Cancelled")

	def test_trip_cancel_after_trip_started(self):
		"""
			Checks if customer can cancel the trip after s/he starts it /  boards the cab.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		trip_started_response = json.loads(customer_action.board_cab(response_for_cab_request["data"]["trip_id"]))
		trip_cancelled_response = json.loads(customer_action.cancel_trip(response_for_cab_request["data"]["trip_id"]))

		self.assertFalse(trip_cancelled_response["is_success"])
		self.assertEqual(trip_cancelled_response["response_code"], 250)
		self.assertEqual(trip_cancelled_response["error_message"], "Trip not requested, not dispatched or already started")