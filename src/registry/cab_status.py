CAB_BOOKED = "B"
CAB_AVAILABLE = "A"

def get_cab_status(status):
	if status is None:
		raise ValueError("Empty status is not acceptable")
	
	if status == CAB_BOOKED:
		return "Booked"

	if status == CAB_AVAILABLE:
		return "Available"

	return "Status not Available"