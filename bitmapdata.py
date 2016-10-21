#==============================================================================
#
#
#	Southclaw's Scavenge and Survive
#
#		Copyright (C) 2016 Barnaby "Southclaw" Keene
#
#		This program is free software: you can redistribute it and/or modify it
#		under the terms of the GNU General Public License as published by the
#		Free Software Foundation, either version 3 of the License, or (at your
#		option) any later version.
#
#		This program is distributed in the hope that it will be useful, but
#		WITHOUT ANY WARRANTY; without even the implied warranty of
#		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#		See the GNU General Public License for more details.
#
#		You should have received a copy of the GNU General Public License along
#		with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#==============================================================================

import sys
import io
from PIL import Image, ImageDraw, ImageColor, ImageFont

map_data = []


def load_bitmap(filename):
	"""
	Loads the bitmap data into memory.
	"""

	print("Loading bitmap...")

	global map_data
	im = Image.open(filename)
	map_data = list(im.getdata())

	print("Loaded bitmap.")


def colour_at(x, y):
	"""
	Returns a colour (r,g,b) value for the specified coordinates.
	"""

	if x < -3000.0 or x > 3000.0 or y > 3000.0 or y < -3000.0:
		return None

	iGridX = (int(x)) + 3000
	iGridY = ((int(y)) - 2999) * -1
	#iDataPos = (iGridY * 6000) + iGridX
	iDataPos = (iGridY * 6144) + iGridX
	#iDataPos = (iGridY * 1536) + iGridX

	try:
		c = map_data[iDataPos]

	except IndexError:
		#print("IndexError: Pos: ", iGridX, iGridY, x, y, "iDataPos:", iDataPos, "Len:", len(map_data))
		return None

	return c


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print("Parameters: bitmap path, x, y")

	else:
		x = float(sys.argv[2])
		y = float(sys.argv[3])

		load_bitmap(sys.argv[1])
		print("Colour at", x, y, "is", colour_at(x, y))
