import sys
from src.fuber_core import utils
from src.pricing import pricing_policies

class Order(object):
	def __init__(self, trip_id, customer_id, distance, time, cab_color=None):
		self.__order_id = utils.get_id()
		self.__trip_id = trip_id
		self.__customer_id = customer_id
		self.__order_amount = self.__get_order_amount(distance, time, cab_color)

	def __get_order_amount(self, distance=0.0, time=0.0, cab_color=None):
		amount = 0.0

		amount += float(pricing_policies.PRICE_DISTANCE_WISE[1] * distance) + float(pricing_policies.PRICE_TIME_WISE[1] * time)

		if cab_color is not None and int(cab_color) in pricing_policies.FIXED_PRICE.keys():
			amount += pricing_policies.FIXED_PRICE[int(cab_color)]

		return amount

	def to_dict(self):
		return {"order_id" : self.__order_id, "order_amount" : self.__order_amount}