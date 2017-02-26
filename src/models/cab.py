import sys
from src.registry import cab_colors, cab_status
import abc

class Cab(object):
	def __init__(self, cab_id, location, cab_registry):
		self._cab_id = cab_id
		self._location = location
		self._status = cab_status.CAB_AVAILABLE # Initial cab status
		self._cab_registry = cab_registry

	def _register_cab(self):
		self._cab_registry.register_cab(self)		

	def get_cab_id(self):
		return self._cab_id

	def get_location(self):
		return self._location

	def update_location(self, location):
		self._location = location

	def update_cab_status(self, status):
		self._status = status

	def get_cab_status(self):
		return self._status

	def allocate(self):
		self._status = cab_status.CAB_BOOKED

	def deallocate(self):
		self._status = cab_status.CAB_AVAILABLE

	@abc.abstractmethod
	def to_dict(self):
		pass
		

class ColoredCab(Cab):
	def __init__(self, cab_id, location, cab_registry, color=None):
		super(ColoredCab, self).__init__(cab_id, location, cab_registry)
		self.__color = cab_colors.get_validated_color(color)
		self._register_cab()

	def get_color(self):
		return self.__color

	def to_dict(self):
		return {"cab_id" : str(self._cab_id), "color" : cab_colors.get_cab_color(self.__color), "status" : str(cab_status.get_cab_status(self._status))}
