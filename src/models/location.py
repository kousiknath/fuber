import sys

class Location(object):
	""" Location object with (x, y) coordinate """
	def __init__(self, x, y): 
		self.__x = x
		self.__y = y

	def get_x(self):
		return self.__x

	def get_y(self):
		return self.__y

	def to_dict(self):
		return {"x" : self.__x, "y" : self.__y}