class InvalidColorException(Exception):
	def __init__(self):
		super(InvalidColorException, self).__init__("Invalid cab color exception!")
		pass