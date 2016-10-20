import bitmapdata

TXWORKSPACE_PATH = "txmap/"

BMP_PATH = TXWORKSPACE_PATH + "gtasa-blank-vector.bmp"


bitmapdata.load_bitmap(BMP_PATH)


print("Getting all colors.")

colors = []

for x in range (-3000, 3000):
	for y in range (-3000, 3000):
		c = bitmapdata.colour_at(x, y)

		if c == None:
			continue
		colors.append(c)
		# ... fill in colour codes for species here
mylist = list(set(colors))
#for i in range(mylist):
#	print("#{0:02x}{1:02x}{2:02x}\n".format(clamp(r), clamp(g), clamp(b)))

print("%d colors found." % len(mylist))

def clamp(x): 
  return max(0, min(x, 255))

