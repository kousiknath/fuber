import uuid
from src.models.location import Location
import math

def get_id():
	return str(uuid.uuid1())

def get_trip_distance(start_location, end_location):
	"""
		Distance will be in kilometer.
	"""
	d =  math.sqrt(pow((float(start_location.get_x()) - float(end_location.get_x())), 2) + pow((float(start_location.get_y()) - float(end_location.get_y())), 2))
	d = float("{0:.2f}".format(d))

	return d

def get_trip_timing(trip_distance):
	"""
		Assumptions: 
		It takes 3 minutes of time to travel 1 KM by a cab.
		Timeunit will be in minute.
	"""
	return float(trip_distance * 3)