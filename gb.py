from PIL import Image
import random

img = Image.new("RGBA", ((640), 1280))

for a in range(random.randint(1000, 3000)):
    img.putpixel((random.randint(0, 639), random.randint(0, 1279)), (0xff, 0xff, 0xff, 0xff))

img.save("bg.png")

