import pygame as pg
import pgplus as pgp
from stats import *
from shop import *
import random
from copy import deepcopy
import math

#gauntlet is many stories (eg campaign)
#story is many levels (eg The beggining)
#level is one level (eg Stage 1)

pg.init()
pgp.init()
window=pg.display.set_mode((0,0),pg.FULLSCREEN)
#indow=pg.display.set_mode((800,600))

wh=window.get_size()
cx=wh[0]//2
cy=wh[1]//2

cx=1920//2
cy=1080//2

cam=pgp.camera(wh,(1920,1080))
run=1

room=0
prevrooms=[]
prevroom=None

clock=pg.time.Clock()

Cbackground=(0,0,150)
CbackgroundPoly=(0,0,200)
CbackgroundLine=(0,0,175)

""" Cbackground="red"
CbackgroundPoly="blue"
CbackgroundLine="green" """

r=pg.Rect(0,300,600,200)
r.centerx=cx

rEquip=pg.Rect(30,900,400,150)

rShop=pg.Rect(30,900,400,150)
rShop.right=1890

rCredits=pg.Rect(0,550,600,200)
rCredits.centerx=cx

rQuit=pg.Rect(0,800,600,200)
rQuit.centerx=cx

popup=0



storyIndex=0
storyButtons=[]
story=[]
storyTilt=0

levelIndex=0
levelButtons=[]
levelTilt=0

rGameFloor=pg.Rect(0,700,1920,380)

t1=pg.Rect(1600,100,300,600)
t2=pg.Rect(20,100,300,600)

mon=0


aimon=0
aieff=0.2





goods=[]
evils=[]



defaultStats={
    "sprite":img[0][0],
    "range":100,
    "mspeed":2,
    "aspeed":60,
    "dmg":10,
    "hp":100,
    "kb":1,
    "p":{}
}

hp1=100
hp2=500

gauntletName=""

completed=[]


unitTilt=0
unitX=0
unitIndex=0

ppVictoryScreen=pgp.advanced.Popup

rPopup=pg.Rect(100,100,1720,880)

surf=pg.Surface((0,0))

numkeys=[
    pg.K_1,
    pg.K_2,
    pg.K_3,
    pg.K_4,
    pg.K_5,
    pg.K_6,
    pg.K_7,
    pg.K_8,
    pg.K_9,
    pg.K_0
]

shopIndex=0
shopTilt=0
shopX=cx-185

shopColor={
    "unit": ["purple","darkviolet","purple4"],
    "upgrade": ["yellow","gold","orange"]
}

from text import font2,font5

shopText={
    "unit": font2.render("UNIT",True,"white"),
    "upgrade": font5.render("UPGRADE",True,"white")
}

shopUpgradeSprite=[
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII",
    "IX",
    "X"
]