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

BMP_PATH = TXWORKSPACE_PATH + "radar_hd.bmp"

chance = {
	"water" : 1,
	"roads" : 2,
	"darkforest" : 2,
	"lightforest" : 5,
	"desert" : 3,
	"grassplanes" : 5
}

on = {
	"water" : 0,
	"roads" : 1,
	"darkforest" : 1,
	"lightforest" : 1,
	"desert" : 1,
	"grassplanes" : 1
}

colors = {
	"water" : [(115, 138, 175)],
	"roads" : [(0, 0, 0)],
	"darkforest" : [(54, 105, 46), (57, 105, 41)],
	"lightforest" : [(123, 138, 57)],
	"desert" : [(156, 135, 115), (156, 132, 115)],
	"grassplanes" : [(115, 138, 57)]
}
def gen_stuff():

	print("Generating stuff...")

	stuff = []
	objects ={
	"water" : [0, 0],
	"roads" : [0, 0],
	"darkforest" : [0, 0],
	"lightforest" : [0, 0],
	"desert" : [0, 0],
	"grassplanes" : [0, 0]
}
	a = 0
	b = 0
	for x in range (-3000, 3000):
		if a != 2:
			a += 1
			continue
		a = 0
		for y in range (-3000, 3000):
			if b != 2:
				b += 1
				continue
			b = 0
			c = bitmapdata.colour_at(x, y)

			if c == None:
				continue

			if c in colors["water"]:
				if on["water"] == 1:
					objects["water"][1] += 1;
					if random.randint(0, 100) < chance["water"]:
						stuff.append(("water", x, y))
						objects["water"][0] += 1;

			elif c in colors["roads"]:
				if on["roads"] == 1:
					objects["roads"][1] += 1;
					if random.randint(0, 100) < chance["roads"]:
						stuff.append(("roads", x, y))
						objects["roads"][0] += 1;

			elif c in colors["darkforest"]:
				if on["darkforest"] == 1:
					objects["darkforest"][1] += 1;
					if random.randint(0, 100) < chance["darkforest"]:
						stuff.append(("darkforest", x, y))
						objects["darkforest"][0] += 1;

			elif c in colors["lightforest"]:
				if on["lightforest"] == 1:
					objects["lightforest"][1] += 1;
					if random.randint(0, 100) < chance["lightforest"]:
						stuff.append(("lightforest", x, y))
						objects["lightforest"][0] += 1;

			elif c in colors["desert"]:
				if on["desert"] == 1:
					objects["desert"][1] += 1;
					if random.randint(0, 100) < chance["desert"]:
						stuff.append(("desert", x, y))
						objects["desert"][0] += 1;

			elif c in colors["grassplanes"]:
				if on["grassplanes"] == 1:
					objects["grassplanes"][1] += 1;
					if random.randint(0, 100) < chance["grassplanes"]:
						stuff.append(("grassplanes", x, y))
						objects["grassplanes"][0] += 1;

			# ... fill in colour codes for species here

	print(objects);

	print("Stuff generated %d." % len(stuff))

	return stuff


def save_stuff(stuff):

	files = ["BC", "FC", "LS", "LV", "SF", "RC", "TR"]
	count = 0

	for name in files:
		count = 0
		with io.open(MAPSDATA_PATH + "/" + name + ".foliage", "w") as f:
			for i in stuff:
				if region.is_point_in(i[1], i[2], name):
					f.write(_CreateFoliage(i[0], i[1], i[2]))
					stuff.remove(i)
					count += 1
			print("Saved", count, "foliages for", name)

	with io.open(MAPSDATA_PATH + "/other.foliage", "w") as f:
		for i in stuff:
				f.write(_CreateFoliage(i[0], i[1], i[2]))
				stuff.remove(i)
				count += 1
		print("Saved", count, "foliages for other")

def _CreateFoliage(t, x, y):
	return ("%s %f %f\n" % (t, x, y))

def draw_stuff(stuff):

	im = Image.open(TXWORKSPACE_PATH + "gtasa-blank-1.0.jpg")
	draw = ImageDraw.Draw(im)

	for i in stuff:
		c = (0, 0, 0)

		if i[0] == "water":
			c = colors["water"][0]
		elif i[0] == "roads":
			c = colors["roads"][0]
		elif i[0] == "darkforest":
			c = colors["darkforest"][0]
		elif i[0] == "lightforest":
			c = colors["lightforest"][0]
		elif i[0] == "desert":
			c = colors["desert"][0]
		elif i[0] == "grassplanes":
			c = colors["grassplanes"][0]

		#Todo: fix this maths

		iGridX = (int(i[1])) + 3000
		iGridY = ((int(i[2])) - 2999) * -1

		draw.ellipse([
			iGridX - 6,#		x0
			iGridY - 6,#		y0
			iGridX + 6,#		x1
			iGridY + 6],#		y1
			outline=(255, 255, 255), fill=c)

	im.save("gtasa-foliage.jpg")

def main():
	print("load_bitmap 1/4")
	bitmapdata.load_bitmap(BMP_PATH)
	print("gen_stuff 2/4")
	stuff = gen_stuff()
	print("draw_stuff 3/4")
	draw_stuff(stuff)
	print("save_stuff 4/4")
	save_stuff(stuff)


from time import time
timeinit = int(time())
if __name__ == '__main__':
	main()
	print("done with %d seconds" % (int(time()) - timeinit))