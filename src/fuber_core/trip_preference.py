from registry import cab_colors

class TripPreference(object):
	"""
		Preferred trip attributes:
		- Cab color
	"""
	def __init__(self):
		self.__cab_color = cab_colors.get_dafault_color()

	def set_cab_color(self, color=None):
		if color is None:
			return
			
		self.__cab_color = color

	def get_cab_color(self):
		return this.__cab_color