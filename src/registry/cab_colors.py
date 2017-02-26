_MAX_COLORS = 2

class CabColor():
	COLOR_WHITE, COLOR_PINK = range(1, _MAX_COLORS + 1)
	_DEFAULT_COLOR = COLOR_WHITE

def get_dafault_color():
	return CabColor._DEFAULT_COLOR

def get_validated_color(color):
	default_color = get_dafault_color()

	if color is None:
		return default_color
		
	if color >= 1 and color <= _MAX_COLORS:
		return color

	return default_color

def get_cab_color(color):
	if color is None:
		raise ValueError("Color can't be None")

	if color == CabColor.COLOR_WHITE:
		return "White(Default)"

	if color == CabColor.COLOR_PINK:
		return "Pink"

	return ""