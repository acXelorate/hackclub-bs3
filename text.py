from consts import *

sFont1Bold="./ASSETS/fontBold.ttf"

font1=pg.font.Font("./ASSETS/font.ttf",100)
font2=pg.font.Font("./ASSETS/font.ttf",75)
font3=pg.font.Font("./ASSETS/font.ttf",30)
font4=pg.font.Font("./ASSETS/font.ttf",50)
font5=pg.font.Font("./ASSETS/font.ttf",60)
font6=pg.font.Font("./ASSETS/font.ttf",200)

tTitle=font1.render("BATTLE STICKS",True,"white")
rtTitle=tTitle.get_rect(centerx=cx,y=10)

tTitle2=font2.render("remastered",True,"white")
rtTitle2=tTitle2.get_rect(centerx=cx,y=110)

tTitleShop=font1.render("The Shop",True,"white")
rtTitleShop=tTitleShop.get_rect(centerx=cx,y=10)

tTitleCredits=font1.render("Credits",True,"white")
rtTitleCredits=tTitleCredits.get_rect(centerx=cx,y=10)

tCredits1=font5.render("Battle Sticks Remastered made by acXelorate",True,"black")

slDiscord="discord.gg/5mAPRvebmr"
lCredits1=pgp.advanced.Link("Discord",[60,220],slDiscord,font5,[0,0,150],[150,150,200],[0,0,255],10)
lCredits2=pgp.advanced.Link("GitHub",[350,220],"github.com/acXelorate",font5,[0,0,150],[150,150,200],[0,0,255],10)

tCredits2=font5.render("Song Credits:",True,"black")
lCredits3=pgp.advanced.Link("Main Menu",[50,370],"youtube.com/watch?v=yYzd3MRnbz0",font5,[0,0,150],[150,150,200],[0,0,255],10)
lCredits4=pgp.advanced.Link("Battle 1",[50,440],"pixabay.com/music/eccentric-quirky-curious-circuits-playful-electronic-music-411246",font5,[0,0,150],[150,150,200],[0,0,255],10)
lCredits5=pgp.advanced.Link("Battle 2",[50,510],"pixabay.com/music/upbeat-the-breakdancing-pixel-293049",font5,[0,0,150],[150,150,200],[0,0,255],10)

tOOB=font1.render("OUT OF BOUNDS",True,"white")
rtOOB=tOOB.get_rect(centerx=cx,centery=cy)

sSfx1="./ASSETS/sfx-1-click.mp3"
sSfx2="./ASSETS/sfx-2-select.mp3"
sSfx3="./ASSETS/sfx-3-buy.wav"
sSfx4="./ASSETS/sfx-4-hit1.wav"
sSfx5="./ASSETS/sfx-5-hit2.mp3"
sSfx6="./ASSETS/sfx-6-tHit1.wav"
sSfx7="./ASSETS/sfx-7-tHit2.wav"

sfx1=pg.mixer.Sound(sSfx1)

sfx3=pg.mixer.Sound(sSfx3)

sSong1="./ASSETS/song1-mainMenu.mp3"
sSong2="./ASSETS/song2-battle1.mp3"

hitSfx=[sSfx4,sSfx5]
hitSfx=[pg.mixer.Sound(i) for i in hitSfx]
for sfx in hitSfx: sfx.set_volume(0.3)

tHitSfx=[sSfx6,sSfx7]
tHitSfx=[pg.mixer.Sound(i) for i in tHitSfx]
for sfx in tHitSfx: sfx.set_volume(0.3)