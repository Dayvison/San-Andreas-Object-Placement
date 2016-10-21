# platform imports
import os
import io
import array
from PIL import Image, ImageDraw, ImageColor, ImageFont
import random

# ss script utilities
import region
import bitmapdata
import modelsizes

TXWORKSPACE_PATH = "txmap/"
MAPSDATA_PATH = "Maps/"

BMP_PATH = TXWORKSPACE_PATH + "gtasa-blank-vector.bmp"

chance = {
	"water" : 1,
	"roads" : 5,
	"darkforest" : 30,
	"lightforest" : 50,
	"desert" : 50,
	"grassplanes" : 50
}

on = {
	"water" : 0,
	"roads" : 1,
	"darkforest" : 1,
	"lightforest" : 1,
	"desert" : 1,
	"grassplanes" : 1
}

objects_radius = [
	(0.0, 40.0),
	(5.0, 50.0),
	(20.0, 100.0),
	(50.0, 150.0)
]

colors = {
	"water" : (115, 138, 175),
	"roads" : (0, 0, 0),
	"darkforest" : (54, 105, 46),
	"lightforest" : (123, 138, 57),
	"desert" : (156, 135, 115),
	"grassplanes" : (115, 138, 57)
}
def gen_stuff():

	print("Generating stuff...")

	stuff = []

	for x in range (-3000, 3000):
		for y in range (-3000, 3000):

			c = bitmapdata.colour_at(x, y)

			if c == None:
				continue

			if c == colors["water"]:
				if on["water"] == 1:
					if random.randint(0, 100) < chance["water"]:
						stuff.append(("water", x, y))

			elif c == colors["roads"]:
				if on["roads"] == 1:
					if random.randint(0, 100) < chance["roads"]:
						stuff.append(("roads", x, y))

			elif c == colors["darkforest"]:
				if on["darkforest"] == 1:
					if random.randint(0, 100) < chance["darkforest"]:
						stuff.append(("darkforest", x, y))

			elif c == colors["lightforest"]:
				if on["lightforest"] == 1:
					if random.randint(0, 100) < chance["lightforest"]:
						stuff.append(("lightforest", x, y))

			elif c == colors["desert"]:
				if on["desert"] == 1:
					if random.randint(0, 100) < chance["desert"]:
						stuff.append(("desert", x, y))

			elif c == colors["grassplanes"]:
				if on["grassplanes"] == 1:
					if random.randint(0, 100) < chance["grassplanes"]:
						stuff.append(("grassplanes", x, y))

			# ... fill in colour codes for species here

	print("Stuff generated %d." % len(stuff))

	return stuff


def save_stuff(stuff):

	files = ["BC", "FC", "LS", "LV", "SF", "RC", "TR"]
	count = 0

	for name in files:
		count = 0
		with io.open(MAPSDATA_PATH + "/" + files + ".foliage", "w") as f:
			for i in stuff:
				if region.is_point_in(i[1], i[2], name):
					f.write(_CreateFoliage(i[0], x, y))
					stuff.remove(i)
					count += 1
			print("Saved", count, "foliages for", name)

	with io.open(MAPSDATA_PATH + "/other.foliage", "w") as f:
		for i in stuff:
				f.write(_CreateFoliage(i[0], x, y))
				stuff.remove(i)
				count += 1
		print("Saved", count, "foliages for other")

def _CreateFoliage(t, x, y):
	streamdistance = 0.0;

	for radius in objects_radius:
		if modelsizes.GetColSphereRadius(model) > radius[0]:
			streamdistance = radius[1]

	return ("%s %f %f %f\n" % (t, x, y, streamdistance))

def draw_stuff(stuff):

	im = Image.open(TXWORKSPACE_PATH + "gtasa-blank-1.0.jpg")
	draw = ImageDraw.Draw(im)

	for i in stuff:
		c = (0, 0, 0)

		if i[0] == "water":
			c = colors["water"]
		elif i[0] == "roads":
			c = colors["roads"]
		elif i[0] == "darkforest":
			c = colors["darkforest"]
		elif i[0] == "lightforest":
			c = colors["lightforest"]
		elif i[0] == "desert":
			c = colors["desert"]
		elif i[0] == "grassplanes":
			c = colors["grassplanes"]

		draw.ellipse([int(i[1] + 3000) - 8, int(6000 - (i[2] + 3000)) - 8, int(i[1] + 3000) + 8, int(6000 - (i[2] + 3000)) + 8], outline=(255, 255, 255), fill=c)
		#draw.ellipse([int(i[1] + 1536) - 8, int(6000 - (i[2] + 1536)) - 8, int(i[1] + 1536) + 8, int(6000 - (i[2] + 1536)) + 8], outline=(255, 255, 255), fill=c)

	im.save("gtasa-foliage.jpg")

def main():

	bitmapdata.load_bitmap(BMP_PATH)

	stuff = gen_stuff()

	draw_stuff(stuff)

	save_stuff(stuff)


from time import time
timeinit = int(time())
if __name__ == '__main__':
	main()
	print("done with %d seconds" % (int(time()) - timeinit))