from PIL import Image

img_name = input("image name = ")

matrix = []

img = Image.open(img_name)

for n,i in enumerate(img.getdata()):
    print(n,i)