from PIL import Image
from PIL import GifImagePlugin

GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

formats = ["PNG","JPEG","GIF"]

filename = input("Filename (with ending): ")

img = Image.open(filename,"r",formats)

img_type = img.format
    
if img_type == "PNG" or img_type == "JPEG":
    
    copy_img = img.convert("RGBA")

    x = copy_img.size[0]
    y = copy_img.size[1]
    
    e = list(copy_img.getdata())
    
    while x*y - e.count((0,0,0,0)) > 128:
        
        x = int(x/1.05)
        y = int(y/1.05)
        
        copy_img = copy_img.resize([x,y])
        
        e = list(copy_img.getdata())
        
    f = open("COPY.txt","w")

    f.write("actions {")
    
    f.write("Global.B = "+str(x)+"; Global.A = "+str(y)+"; ")

    f.write("Global.C = Array(\n")

    for i in range(x*y):
        f.write("Custom color"+str(e[i]))
        if i < x*y-1:
            f.write(",\n")

    f.write(");")

    f.write("}")

    f.close()

elif img_type =="GIF":

    duration = img.info["duration"]

    x = img.size[0]
    y = img.size[1]
    
    while x*y > 128:
        
        x = int(x/1.05)
        y = int(y/1.05)

    frames = []

    subroutines = []

    rules = []

    size = x, y

    for i in range(img.n_frames):

        img.seek(i)
        copy_img = img.copy()
        copy_img.thumbnail(size)
        frames.append(list(copy_img.getdata()))

        subroutines.append(str(i+8)+": Frame"+str(i+1)+" ")

        rules.append("Frame"+str(i+1))

    f = open("COPY.txt","w")

    f.write("subroutines{\n")
        
    for i in subroutines:
        f.write(i+"\n")

    f.write("}\n")

    f.write('rule("GIF loop"){event{Ongoing - Each Player;All;All;}conditions{Event Player.D == True;Event Player == Host Player;}actions{\n')
    for i in range(len(rules)):
        f.write('Start Rule('+rules[i]+', Do Nothing);\n')
        f.write('Wait(Global.E, Abort when False);')

    f.write("Loop if condition is true;")

    f.write("}}")
    
    for i in range(len(rules)):
        f.write('rule("'+rules[i]+'"){event{Subroutine;'+rules[i]+';}')
        f.write('actions{ Global.B = '+str(x)+'; Global.A ='+str(y)+'; Global.E ='+str(duration/1000)+'; Global.C = Array(')

        for o in range(x*y):
            if img.mode == "RGB":
                frames[i][o] = frames[i][o] + (255,)
            f.write("Custom color"+str(frames[i][o]))
            if o < x*y-1:
                f.write(",\n")

        f.write(");}}\n")                

    f.close()

