# platform imports
import os
import io
import array
from PIL import Image, ImageDraw, ImageColor, ImageFont
import random

# ss script utilities
import region
import mapandreas
import bitmapdata
import modelsizes

TXWORKSPACE_PATH = "txmap/"
MAPSDATA_PATH = "Maps/"

HMAP_PATH = "SAfull.hmap"
BMP_PATH = TXWORKSPACE_PATH + "gtasa-blank-vector.bmp"

chance = {
	"water" : 1,
	"roads" : 5,
	"darkforest" : 30,
	"lightforest" : 50,
	"desert" : 50,
	"grassplanes" : 50
}
objects_radius = [
	(0.0, 40.0),
	(5.0, 50.0),
	(20.0, 100.0),
	(50.0, 150.0)
]

colors = {
	"water" : (0, 0, 0),
	"roads" : (0, 0, 0),
	"darkforest" : (0, 0, 0),
	"lightforest" : (0, 0, 0),
	"desert" : (0, 0, 0),
	"grassplanes" : (0, 0, 0)
}

obj_arr_E_WATER = [1242, 1242]
obj_arr_E_ROADS = [18862, 647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827]
obj_arr_E_DARKFOREST = [647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827]
obj_arr_LIGHTFOREST = [654, 655, 656, 657, 658, 659, 660, 661]
obj_arr_DESERT = [647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827]
obj_arr_E_GRASSPLANES = [647, 692, 759, 760, 762, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827]


def gen_stuff():

	print("Generating stuff...")

	stuff = []
	z = 0.0

	for x in range (-3000, 3000):
		for y in range (-3000, 3000):

			c = bitmapdata.colour_at(x, y)

			if c == None:
				continue

			# water			:
			# roads			:
			# darkforest	: 96
			# lightforest	: 128
			# desert		: 160
			# grassplanes	: 192

			if c == colors["water"]:
				if random.randint(0, 100) < chance["water"]:
					z = mapandreas.get_z(x, y) - 0.5
					stuff.append(("water", x, y, z))

			elif c == colors["roads"]:
				if random.randint(0, 100) < chance["roads"]:
					z = mapandreas.get_z(x, y) - 0.5
					stuff.append(("roads", x, y, z))

			elif c == colors["darkforest"]:
				if random.randint(0, 100) < chance["darkforest"]:
					z = mapandreas.get_z(x, y) - 0.5
					stuff.append(("darkforest", x, y, z))

			elif c == colors["lightforest"]:
				if random.randint(0, 100) < chance["lightforest"]:
					z = mapandreas.get_z(x, y) - 0.5
					stuff.append(("lightforest", x, y, z))

			elif c == colors["desert"]:
				if random.randint(0, 100) < chance["desert"]:
					z = mapandreas.get_z(x, y) - 0.5
					stuff.append(("desert", x, y, z))

			elif c == colors["grassplanes"]:
				if random.randint(0, 100) < chance["grassplanes"]:
					z = mapandreas.get_z(x, y) - 0.5
					stuff.append(("grassplanes", x, y, z))

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
					f.write(_CreateFoliage(i[0], x, y, z))
					stuff.remove(i)
					count += 1
			print("Saved", count, "foliages for", name)

	with io.open(MAPSDATA_PATH + "/other.foliage", "w") as f:
		for i in stuff:
				f.write(_CreateFoliage(i[0], x, y, z))
				stuff.remove(i)
				count += 1
		print("Saved", count, "foliages for other")

def _CreateFoliage(t, x, y, z):
	model = 0

	if t == "water":
		model = random.choice(obj_arr_E_WATER)
	elif t == "roads":
		model = random.choice(obj_arr_E_ROADS)
	elif t == "darkforest":
		model = random.choice(obj_arr_E_DARKFOREST)
	elif t == "lightforest":
		model = random.choice(obj_arr_LIGHTFOREST)
	elif t == "desert":
		model = random.choice(obj_arr_DESERT)
	elif t == "grassplanes":
		model = random.choice(obj_arr_E_GRASSPLANES)

	streamdistance = 0.0;

	for radius in objects_radius:
		if modelsizes.GetColSphereRadius(model) > radius[0]:
			streamdistance = radius[1]

	return ("CreateDynamicObject(%d, %f, %f, %f, 0.0, 0.0, 0.0, .streamdistance = %f);" % (model, x, y, z, streamdistance))

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
	
	mapandreas.load_heightmap(HMAP_PATH)

	bitmapdata.load_bitmap(BMP_PATH)

	stuff = gen_stuff()

	draw_stuff(stuff)

	save_stuff(stuff)


if __name__ == '__main__':
	main()
