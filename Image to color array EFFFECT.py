from PIL import Image

z = 0

img = Image.open(input("Filename (without type): ")+".png")

img_x = img.size[0]
img_y = img.size[1]

while img_x*img_y > 256:
    img_x = int(img_x/1.25)
    img_y = int(img_y/1.25)

newimg = img.resize([img_x,img_y])

newimg = newimg.convert("RGBA")

pixels = newimg.load()

f = open("COPY.txt","w")

f.write("actions{Event Player.B ="+str(img_x)+";Event Player.A ="+str(img_y)+";Global.C = Array(")

for y in range(img_y):
    for x in range(img_x):
        z+=1
        f.write("Custom color("+str(pixels[x,y][0])+","+str(pixels[x,y][1])+","+str(pixels[x,y][2])+","+str(pixels[x,y][3])+")")
        if z<img_x*img_y:
            f.write(",\n")

f.write(");}")

f.close()

