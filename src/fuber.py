import sys

from registry.cab_registry import CabRegistry
from registry.customer_registry import CustomerRegistry
from registry.trip_registry import TripRegistry
from registry import cab_colors
from registry.cab_colors import CabColor
import random
import decimal
from models.location import Location
from models.cab import ColoredCab
from models.customer import Customer

from fuber_core.cab_dispatcher import CabDispatcher
from fuber_core.trip_dispatcher import TripDispatcher
from fuber_core.customer_actions import CustomerAction

import json

class Fuber(object):
	def __init__(self):
		pass

	def start(self):
		cab_registry = CabRegistry()
		customer_registry = CustomerRegistry()

		print '------ creating cabs ---'

		for i in range(1, 100):
			location_x = decimal.Decimal(random.randrange(50000))/100
			location_y = decimal.Decimal(random.randrange(10000))/100
			loc = Location(location_x, location_y)
			color = cab_colors.get_dafault_color()

			c = ColoredCab(i, loc, cab_registry, color)

		for i in range(200, 250):
			location_x = decimal.Decimal(random.randrange(20000))/100
			location_y = decimal.Decimal(random.randrange(30000))/100
			loc = Location(location_x, location_y)
			color = CabColor.COLOR_PINK

			c = ColoredCab(i, loc, cab_registry, color)

		cab_registry.get_all_registered_cabs()

		print '----- creating customers ------'

		for i in range (1000, 1010):
			cst = Customer(i, 'test', 'test@test.com', customer_registry)

		customer_registry.get_all_registered_customers()

		trip_registry = TripRegistry()
		cb_dispatcher = CabDispatcher(cab_registry)
		trip_dispatcher = TripDispatcher(cb_dispatcher, trip_registry)

		customer_action = CustomerAction(1000, trip_dispatcher)
		dispatched_trip = customer_action.request_cab(Location(66.34, 100.34), Location(34.43, 89.1), None)

		customer_action = CustomerAction(1009, trip_dispatcher)
		cab_request_response = customer_action.request_cab(Location(23.34, 100.34), Location(78.43, 32.10), None)

		json_cab_requested_response = json.loads(cab_request_response)
		trip_started_response = customer_action.onboard_cab(json_cab_requested_response["data"]["trip_id"])
		trip_finished_response = customer_action.make_payment_and_offboard(json_cab_requested_response["data"]["trip_id"])
		# trip_cancelled_response = customer_action.cancel_trip(json_cab_requested_response["data"]["trip_id"])

		print trip_started_response


if __name__ == '__main__':
	f = Fuber()
	f.start()