import json

class CabRegistry(object):
	"""
		Central cab register
	"""
	def __init__(self):
		self.__registry = dict()
		self.__registry_by_color = dict()

	def register_cab(self, cab_obj):
		_id = int(cab_obj.get_cab_id())
		_color = int(cab_obj.get_color())

		self.__registry[_id] = cab_obj
		
		if _color not in self.__registry_by_color or self.__registry_by_color[_color] is None:
			self.__registry_by_color[_color] = set()

		self.__registry_by_color[_color].add(_id)

	def get_cab_information(self, cab_id):
		if cab_id is None:
			return

		if cab_id not in self.__registry:
			raise ValueError("No suitable cab found !!!")

		return self.__registry[cab_id]

	def get_all_registered_cabs_by_color(self, color_index=None):
		result = list()

		if color_index is None or color_index <= 0:
			return result

		if self.__registry_by_color is None or len(self.__registry_by_color) == 0 or color_index not in self.__registry_by_color:
			return result

		for cab_id in self.__registry_by_color[color_index]:
			result.append(self.__registry[cab_id])

		return result

	def get_all_registered_cabs(self):
		result = list()
		if self.__registry is None or len(self.__registry) == 0:
			return result

		return list(self.__registry.values())