from PIL import Image


im = Image.open("all.png")
imgwidth, imgheight = im.size
cuts = 5
height = int(imgheight / cuts)
k = 0
for i in range(0, imgheight, height):
    box = (0, i, imgwidth, i+height)
    a = im.crop(box)
    a.save(f"test_{k}.png")
    k +=1
