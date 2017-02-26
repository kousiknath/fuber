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

class CabsTest(unittest.TestCase):
	def setUp(self):
		self.__cab_registry = CabRegistry()
		self.__customer_registry = CustomerRegistry()
		self.__trip_registry = TripRegistry()
		self.__cab_dispatcher = CabDispatcher(self.__cab_registry)
		self.__trip_dispatcher = TripDispatcher(self.__cab_dispatcher, self.__trip_registry)

	def test_request_cab(self):
		"""
			When cab gets assigned to a customer, it's in booked state till trip gets completed or cancelled.
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
		self.assertEqual(response_for_cab_request["data"]["cab_info"]["status"], "Booked")

	def test_cab_status_after_trip_started(self):
		"""
			When cab gets assigned to a customer, it's in booked state till trip gets completed or cancelled.
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
		self.assertEqual(trip_started_response["error_message"], "")
		self.assertEqual(trip_started_response["data"]["cab_info"]["status"], "Booked")

	def test_cab_status_after_trip_cancelled(self):
		"""
			After trip gets cancelled, cab should become available.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		trip_cancelled_response = json.loads(customer_action.cancel_trip(response_for_cab_request["data"]["trip_id"]))

		self.assertEqual(trip_cancelled_response["data"]["cab_info"]["status"], "Available")

	def test_cab_location_after_trip_completed(self):
		"""
			After trip completion, the cab location should be as same as the customer drop location as the cab is 
			suppossed to wait around outside the customers house.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		trip_started_response = json.loads(customer_action.board_cab(response_for_cab_request["data"]["trip_id"]))
		trip_finished_response = json.loads(customer_action.make_payment_and_offboard(response_for_cab_request["data"]["trip_id"]))

		cab_id = trip_finished_response["data"]["cab_info"]["cab_id"]
		cab_obj = self.__cab_registry.get_cab_information(int(cab_id))
		final_cab_location = cab_obj.get_location()
		
		self.assertEqual(final_cab_location.get_x(), customer_drop_location.get_x())
		self.assertEqual(final_cab_location.get_y(), customer_drop_location.get_y())

	def test_rebooking_same_cab(self):
		"""
			When a cab is booked, it should not get rebooked untill it becomes available.
			This test case contains only one registered cab with 2 nearby customers requesting for the same.
		"""
		customer_pickup_location = Location(12.45, 34.55)
		customer_drop_location = Location(45.32, 67.676)

		test_cab_location = Location(10.00, 21.23)
		color = cab_colors.get_dafault_color()
		c = ColoredCab(0, test_cab_location, self.__cab_registry, color)

		customer_action = CustomerAction.get_action_object(customer_id = 100, trip_dispatcher = self.__trip_dispatcher)
		response_for_cab_request = json.loads(customer_action.request_cab(customer_pickup_location, customer_drop_location))
		
		another_customer_pickup_location = Location(11.35, 37.12)
		another_customer_drop_location = Location(42.62, 68.0)

		another_customer_action = CustomerAction.get_action_object(customer_id = 101, trip_dispatcher = self.__trip_dispatcher)
		another_cab_request_response = json.loads(another_customer_action.request_cab(another_customer_pickup_location, another_customer_drop_location))

		self.assertFalse(another_cab_request_response["is_success"])
		self.assertEqual(another_cab_request_response["error_message"], "No cab can be allocated")	

if __name__ == "__main__":
	unittest.main()