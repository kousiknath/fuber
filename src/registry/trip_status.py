TRIP_DISPATCHED = "D"
TRIP_CANCELLED = "C"
TRIP_STARTED = "S"
TRIP_COMPLETED = "E"
TRIP_ALLOCATION_FAILED = "F"

def get_trip_status(status):
	if status is None:
		raise ValueError("status can't be None")

	if status == TRIP_DISPATCHED:
		return "Trip Allocated"

	if status == TRIP_CANCELLED:
		return "Trip Cancelled"

	if status == TRIP_STARTED:
		return "Trip Started"

	if status == TRIP_COMPLETED:
		return "Trip Completed"

	if status == TRIP_ALLOCATION_FAILED:
		return "No Cab Available"

	return "Trip Status Not Available"