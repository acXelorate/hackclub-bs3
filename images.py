from consts import *


def quickload(path):
    return pg.image.load(f"./ASSETS/{path}").convert_alpha()

imgBG=quickload("background.png")

bg=[
    quickload("bg1.png")
]

floor=[
    quickload("floor1.png")
]

tower=[
    quickload("tower1.png")
]

new=[]
for t in tower:
    new.append([t,pg.transform.flip(t,1,0)])
    
tower=new