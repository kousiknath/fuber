import sys
from src.fuber_core.cab_actions import CabAction
from src.registry import cab_colors, cab_status
import heapq
import utils
import cab_dispatcher_settings

class CabDispatcher(object):
	def __init__(self, cab_registry, *args, **kwargs):
		self.__cab_registry = cab_registry
		self.__args = args
		self.__kwargs = kwargs

	def allocate_cab_if_available(self, customer_location, trip_preference, *args, **kwargs):
		"""
			Find suitable cab from cab registry, wrap it in cab action and return.
		"""
		allocated_cab_id = self.__allocate(customer_location, trip_preference, *args, **kwargs)
		allocated_cab = self.__cab_registry.get_cab_information(allocated_cab_id)
		cab_action = CabAction(allocated_cab)
		cab_action.allocate_cab()

		return cab_action

	def __allocate(self, customer_location, trip_preference, *args, **kwargs):
		cab_color = trip_preference.get_cab_color()
		all_cabs = list()

		"""
			With default cab color (color = 1) or with no particular color selection, all registered cabs will be searched
			to find available cabs.
		"""

		if cab_color is None or int(cab_color) == 1:
			all_cabs = self.__cab_registry.get_all_registered_cabs()
		else:
			all_cabs = self.__cab_registry.get_all_registered_cabs_by_color(cab_color)

		min_heap = list()

		for a_cab in all_cabs:
			if a_cab.get_cab_status() == cab_status.CAB_BOOKED:
				continue

			cab_distance =  utils.get_trip_distance(customer_location, a_cab.get_location())
			
			if cab_distance > float(cab_dispatcher_settings.CAB_SEARCH_RADIUS):
				continue

			# Heap tuple - (distance, cab_id) - heap will be sorted based on first parameter (distance) of the tuples.
			heapq.heappush(min_heap, (cab_distance, a_cab.get_cab_id()))

		available_cabs = heapq.nsmallest(cab_dispatcher_settings.MINIMUM_CABS_TO_SHOW, min_heap)

		if available_cabs is None or len(available_cabs) == 0:
			return None

		return available_cabs[0][1] # return the cab id
