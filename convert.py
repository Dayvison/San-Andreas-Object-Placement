#!/usr/bin/python3
from PIL import Image


file = "txmap/radar_hd"

inputfile = file + ".png"
outputfile = file + ".bmp"

img = Image.open(inputfile)

print(len(img.split()))
# prevent IOError: cannot write mode RGBA as BMP
if len(img.split()) == 4:
	print("Connot write mode RGBA as BMP")
	r, g, b, a = img.split()
	img = Image.merge("RGB", (r, g, b))
	img.save(outputfile)
else:
	print("Write mode RGBA as BMP")
	img.save(outputfile)