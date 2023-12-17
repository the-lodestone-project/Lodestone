from PIL import Image 
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("images") if isfile(join("images", f))]


for image in onlyfiles:
    im = Image.open(f"images/{image}")
    im = im.resize((128,128), resample=Image.NEAREST)
    im.save(f"upscaled/{image}")
    print(image)