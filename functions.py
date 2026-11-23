from consts import *
from images import *
from text import *
from classes import *
from stats import *
import json

backgroundx=0
oldmon=0

def cdCondition(loadoutdict):
    """loadoutdict[index]"""
    return loadoutdict["tick"]>=loadoutdict["cd"]

def getCondition(mon,loadout,loadoutdict,cdcondition):
    """loadoutdict[index] and loadout[index]"""
    return loadout!=None and mon>=loadoutdict["cost"] and cdcondition

class visual:
    @staticmethod
    def backgroundEffect():
        global backgroundx
        
        pgp.blit(window,cam,imgBG,0,0)
        
        for i in range(5):
            p1=[backgroundx      +800*i,0]
            p2=[backgroundx+600  +800*i,0]
            p3=[backgroundx-600  +800*i,1080]
            p4=[backgroundx      +800*i,1080]
            pgp.draw.polygon(window,cam,CbackgroundPoly,[p1,p2,p4,p3,p1])
            pgp.draw.line(window,cam,CbackgroundLine,p1,p3,10)
            pgp.draw.line(window,cam,CbackgroundLine,p2,p4,10)
            #pgp.draw.rect(window,cam,"red",[p2[0],p2[1],10,10])
        
        backgroundx-=1
        if backgroundx<-800: backgroundx=0
        
    @staticmethod
    def drawTitle():
        pgp.blit(window,cam,tTitle,rtTitle)
        pgp.blit(window,cam,tTitle2,rtTitle2)
        
    @staticmethod
    def drawTitleShop(xp):
        pgp.blit(window,cam,tTitleShop,rtTitleShop)
        
        txt=font2.render(f"{xp}xp",True,"white")
        rTxt=txt.get_rect(right=1920)
        pgp.blit(window,cam,txt,rTxt)
        
        
    @staticmethod
    def drawTitleCredits():
        pgp.blit(window,cam,tTitleCredits,rtTitleCredits)
        pgp.draw.rect(window,cam,"white",pg.Rect(45,145,1820,900),border_radius=20)
        pgp.draw.rect(window,cam,"black",pg.Rect(45,145,1820,900),5,border_radius=20)
        
    @staticmethod
    def drawInGameBackground():
        window.fill("blue")
        pgp.blit(window,cam,bg[0],0,0)
        pgp.draw.rect(window,cam,"green",rGameFloor)
        pgp.blit(window,cam,floor[0],0,700)
        
    @staticmethod
    def drawMoney(level,mon):
        txt=font2.render(f"{round(mon)}$",True,"white")
        rect=txt.get_rect(y=0,right=1900)
        pgp.blit(window,cam,txt,rect)
        
        txt=font2.render(level["name"],True,"white")
        pgp.blit(window,cam,txt,0,0)
    
    @staticmethod
    def drawCastle(hp1,hp2):
        #pgp.draw.rect(window,cam,"gray",t1,gui=False)
        #pgp.draw.rect(window,cam,"gray",t2,gui=False)
        
        pgp.blit(window,cam,tower[0][0],t1)
        pgp.blit(window,cam,tower[0][1],t2)
        
        txt=font4.render(f"{hp1} hp",True,"white")
        rTxt=txt.get_rect(y=t1.y+25,centerx=t1.centerx)
        pgp.blit(window,cam,txt,rTxt,gui=False)
        
        txt=font4.render(f"{hp2} hp",True,"white")
        rTxt=txt.get_rect(y=t2.y+25,centerx=t2.centerx)
        pgp.blit(window,cam,txt,rTxt,gui=False)
    
    @staticmethod    
    def drawPortraits(loadoutdict,mousex,mousey,leftclick,mon,research,keys):
        global oldmon
        
        """Returns new mon"""
        index=0
        y=705
        for _ in range(2):
            x=335
            for _ in range(5):
                rect=pg.Rect(x,y,180,180)
                loadout=[i["index"] for i in loadoutdict]
                cdcondition=cdCondition(loadoutdict[index])
                condition=getCondition(mon,loadout[index],loadoutdict[index],cdcondition)
                
                if not cdcondition:
                    loadoutdict[index]["tick"]+=research/4
                    if condition==False and getCondition(mon,loadout[index],loadoutdict[index],cdCondition(loadoutdict[index]))==True:
                        condition=True
                        sfx1.play()
                        
                if condition and not getCondition(oldmon,loadout,loadoutdict[index],cdCondition):
                    sfx1.play()
                
                
                pgp.draw.rect(window,cam,"white" if condition else "gray",rect)
                pgp.draw.rect(window,cam,"black",rect,3)
                
                try:
                    pgp.blit(window,cam,img[stats.index(loadout[index])][1],rect)
                except: pass
                
                if not cdcondition:
                    pgp.draw.rect(window,cam,"black",pg.Rect(x+10,y+10,160,30))
                    pgp.draw.rect(window,cam,"blue",pg.Rect(x+12,y+12,loadoutdict[index]["tick"]*156//loadoutdict[index]["cd"],26))
                
                if loadout[index]!=None:
                    txt=font3.render(f"{loadoutdict[index]["cost"]}$",True,"black")
                    rtxt=txt.get_rect(bottomright=rect.bottomright)
                    pgp.blit(window,cam,txt,rtxt)
                
                if ((leftclick and pgp.rect.collidepoint(cam,rect,mousex,mousey)) or keys[numkeys[index]]) and condition:
                    goods.append(Unit(pg.Rect(1600,550,150,150),-1,loadout[index]))
                    mon-=loadoutdict[index]["cost"]
                    loadoutdict[index]["tick"]=0
                    channel = pg.mixer.find_channel(True)
                    channel.play(sfx3)
                
                x+=250
                index+=1
            y=890
        oldmon=mon
        return mon
    
    @staticmethod
    def drawLoadout(loadout,goodlist,unitX,unitIndex,unitTilt,left,right,enter,keys,mousex,mousey,leftclick,rightclick):
        """Returns loadout, unitX, unitTilt, unitIndex"""
        i=0
        
        for y in range(20,780,380):
            for x in range(20,1920,380):
                rect=pg.Rect(x,y,360,360)
                
                pgp.draw.rect(window,cam,"white",rect)
                pgp.draw.rect(window,cam,"black",rect,5)
    
                if loadout[i]!=None:
                    pgp.blit(window,cam,pg.transform.scale(img[loadout[i]][1],(360,360)),rect)
                
                i+=1
                
        pgp.draw.rect(window,cam,"yellow",pg.Rect(cx-95,795,190,190),5)
        x=cx-90-unitX
        
        if unitTilt!=0:
            unitX+=40*pgp.pyplus.getState(unitTilt)
            unitTilt-=40*pgp.pyplus.getState(unitTilt)
            
        lastUnlockedUnit=-1
        for i in range(len(stats)):
            if i in goodlist:
                lastUnlockedUnit+=1
        
        if left and unitIndex!=0 and unitTilt==0:
            unitIndex-=1
            unitTilt=-200
            
        
            
        elif right and unitIndex!=lastUnlockedUnit and unitTilt==0:
            unitIndex+=1
            unitTilt=200
            
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            for i,key in enumerate(numkeys):
                if keys[key]:
                    loadout[i]=None
            
        for i in range(len(stats)):
            if i in goodlist:
                rect=pg.Rect(x,800,180,180)
                pgp.draw.rect(window,cam,"white" if i not in loadout else "gray",rect)
                pgp.draw.rect(window,cam,"black",rect,5)
                pgp.blit(window,cam,img[i][1],rect)
                
                if x==cx-90 and i not in loadout:
                    if enter:
                        for o,slot in enumerate(loadout):
                            if slot is None:
                                loadout[o]=i
                                break
                            
                    for o,key in enumerate(numkeys):
                        if keys[key]:
                            if not keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                                loadout[o]=i
                        
                if pgp.rect.collidepoint(cam,rect,mousex,mousey):
                    if leftclick and i not in loadout:
                        for o,slot in enumerate(loadout):
                            if slot is None:
                                loadout[o]=i
                                break
                    if rightclick and i in loadout:
                        for o,slot in enumerate(loadout):
                            if slot==i:
                                loadout[o]=None
                
                x+=200
                
                
                
        return loadout,unitX,unitTilt,unitIndex

    
def buttonStep(button:pgp.advanced.Button,popup,window,cam,mousex,mousey,leftclick):
    if popup==0:
        if button.text=="Credits": print(button.Rect)
        button.step(window,cam,mousex,mousey,leftclick)
        
    else:
        pgp.draw.button(window,cam,button)
        
def linkStep(link:pgp.advanced.Link,popup,window,cam,mousex,mousey,leftclick):
    if popup==0:
        link.step(window,cam,mousex,mousey,leftclick)

    else:
        link.draw(window,cam,False)
        
def ai(level,aimon1,aimon2,evils,ai2choice):
    aimon1+=level["aieff1"]
    aimon2+=level["aieff2"]
    
    #ai1 -> tries to buy random character every frame
    ai1choice=random.choice(level["enemies"])
    if aimon1>=stats[ai1choice]["cost"] and random.randint(0,60)==0:
        aimon1-=stats[ai1choice]["cost"]
        evils.append(Unit(pg.Rect(170,550,150,150),1,stats[ai1choice]))
    
    #ai2 saves up for random character
    if ai2choice==None:
        ai2choice=random.choice(level["enemies"])
    else:
        if aimon2>=stats[ai2choice]["cost"]:
            aimon2-=stats[ai2choice]["cost"]
            evils.append(Unit(pg.Rect(170,550,150,150),1,stats[ai2choice]))
            ai2choice=None
            
    return aimon1,aimon2,ai2choice

class Json:
    @staticmethod
    def save(data,name):
        with open(name,"w",encoding="utf-8") as file:
            json.dump(data,file,indent=4)
            
    @staticmethod
    def load(name):
        with open(name,"r",encoding="utf-8") as file:
            return json.load(file)
        
selectedSong=""
def playSong(name,loops:int=0,volume:float=1,restart=False):
    """Volume is 0.0-1.0 (0.1,0.20,0.33...)"""
    global selectedSong
    if selectedSong!=name or restart:
        pg.mixer_music.load(name)
        pg.mixer_music.play(loops)
        pg.mixer_music.set_volume(volume)
        selectedSong=name