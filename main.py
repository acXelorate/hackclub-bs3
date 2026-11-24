import os
import sys

if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

from consts import *
from functions import *
from classes import *
from campaign import *



v=1.0
defaultData["version"]=v

playSong(sSong1,-1,0.2)

def loadData():
    global stages,completed,goodlist,equip,research,efficiency,fLoadout,fShop,xp
    data=Json.load("save.json")
    if data["version"]<v:
        data=defaultData|data
    stages=data["stages"]
    completed=data["completed"]
    goodlist=data["units"]
    equip=data["loadout"]
    research=data["research"]
    efficiency=data["efficiency"]
    fLoadout=data["fLoadout"]
    fShop=data["fShop"]
    xp=data["xp"]
    
def saveData():
    data={
        "version":v,
        "stages":stages,
        "completed":completed,
        "units":goodlist,
        "loadout":equip,
        "research":research,
        "efficiency":efficiency,
        "fLoadout":fLoadout,
        "fShop":fShop,
        "xp":xp
    }
    Json.save(data,"save.json")

if not pgp.pyplus.fileExists("save.json"):
    Json.save(defaultData,"save.json")
    newGame=1
    popup=5
else:
    newGame=0
loadData()

def goto(num,flags=None):
    if type(flags)!=list:
        flags=[flags]
    global room,prevrooms,leftclick
    leftclick=0
    if room!=4:
        prevrooms.append(room)
    else:
        prevrooms.pop(-1)
    room=num
    
    if "closePopup" in flags:
        closePopup()
    
    if num==2:
        global storyIndex,storyButtons
        storyIndex=0
        storyButtons=getStoryButtons(campaign)
        
        if flags!=[None]:
            global gauntletName
            gauntletName=flags[0]
        
    if num==3:
        global levelIndex,levelButtons
        if "ignore" not in flags and "keepIndex" not in flags: levelIndex=0
        if not "ignore" in flags:
            levelButtons=getLevelButtons(story,True if "keepIndex" in flags else False)
        
    if num==4:
        global hp1,hp2,loadout,goods,evils,mon,eff,aimon1,aimon2,ai2choice
        
        if "song" not in level:
            song=sSong2
        playSong(song,-1,0.2,True)
        
        ai2choice=None
        
        hp1=100
        hp2=level["hp"]
        
        mon=0
        eff=0.5*(1+efficiency/5 if efficiency>1 else 1)
        
        aimon1=0
        aimon2=0
        
        goods[:]=[]
        evils[:]=[]
        
        loadout=[
            {
                "index":stats[i],
                "cost":stats[i]["cost"],
                "cd":stats[i]["cd"],
                "tick":stats[i]["cd"]
            } if i!=None else
            {
                "index":None,
                "cost":0,
                "cd":0,
                "tick":0
            } for i in equip
        ]
        
    else:
        playSong(sSong1,-1,0.2)
    
def goback(flags=None):
    global room,popup
    if room!=4:
        if flags=="closePopup": popup=0
        if prevrooms!=[]:
            room=prevrooms[-1]
            prevrooms.pop(-1)
        else:
            popup=1
    else: popup=4
    
def closePopup():
    global popup
    popup=0
    
def Quit():
    global run
    run=0

def setPopup(num,flags=None):
    global popup
    if flags=="disableLeftclick":
        global leftclick
        leftclick=0
    popup=num

def selectStory(gauntlet,storyIndex):
    global story
    
    
    story=gauntlet[storyIndex]
    
    goto(3)
    
    
    
def selectLevel(_level):
    global level
    level=_level
    goto(4)

def getStoryButtons(gauntlet:list):
    
    buttons=[]
    i=0
    for o,story in enumerate(gauntlet):
        if not any(u[1]==o for u in stages):
            continue
        buttons.append(pgp.advanced.Button(
            pg.Rect(cx-400,400+i*400,800,300),
            story["name"],
            selectStory,
            fontName=sFont1Bold,
            fontSize=75,
            hoverEffect="popup",
            borderRadius=20,
            flags={"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[gauntlet,i]}
        ))
        i+=1
    return buttons

def getLevelButtons(story,flags):
    buttons=[]
    
    if gauntletName=="campaign":
        gauntlet=campaign
    storyIndex=gauntlet.index(story)
    
    if flags==False:
        x=0
    else:
        x=700*levelIndex
    
    for i,level in enumerate(story["levels"]):
        rect=pg.Rect(cx-300+i*700-x,400,600,200)
        
        if [gauntletName,storyIndex,i] in stages:
        
            buttons.append(pgp.advanced.Button(
                rect,
                level["name"],
                selectLevel,
                fontName=sFont1Bold,
                fontSize=75,
                hoverEffect="popup",
                borderRadius=20,
                flags={"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[story["levels"][i]]}
            ))
            
        else:
            buttons.append(pgp.advanced.Button(
                rect,
                "???",
                lambda: None,
                bgColor="gray",
                fontName=sFont1Bold,
                fontSize=75,
                hoverEffect="popup",
                borderRadius=20,
                flags={"hoverSfx":sSfx1}
            ))
            
    return buttons

bPlay=pgp.advanced.Button(r,"PLAY",goto,"white",CbackgroundLine,"black","Font",sFont1Bold,75,"popup",20,{"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[1]})
bCredits=pgp.advanced.Button(rCredits,"Credits",goto,"white",CbackgroundLine,"black","Font",sFont1Bold,75,"popup",20,{"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[7]})
bQuit=pgp.advanced.Button(rQuit,"Quit",setPopup,"white",CbackgroundLine,"black","Font",sFont1Bold,75,"popup",20,{"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[1,"disableLeftclick"]})
bCampaign=pgp.advanced.Button(r,"Campaign",goto,"white",CbackgroundLine,"black","Font",sFont1Bold,75,"popup",20,{"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[2,"campaign"]})
bEquip=pgp.advanced.Button(rEquip,"Loadout",goto,lineColor=CbackgroundLine,fontSize=75,fontName=sFont1Bold,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[5]})
bShop=pgp.advanced.Button(rShop,"Shop",goto,lineColor=CbackgroundLine,fontSize=75,fontName=sFont1Bold,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"clickSfx":sSfx2,"functionParameters":[6]})

ppQuit=pgp.advanced.Popup(rPopup,font2.render("Are you sure you want to quit",True,"black"),
                          buttons=[
                              pgp.advanced.Button(pg.Rect(100,650,700,200),"Yes",Quit,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1}),
                              pgp.advanced.Button(pg.Rect(900,650,700,200),"No",closePopup,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1})
                              ],
                          borderRadius=20)

ppPause=pgp.advanced.Popup(rPopup,font2.render("Game Paused",True,"black"),
buttons=[
    pgp.advanced.Button(pg.Rect(50,650,500,200),"Exit",goto,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"functionParameters":[3,["closePopup","ignore"]]}),
    pgp.advanced.Button(pg.Rect(600,650,500,200),"Back",closePopup,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1}),
    pgp.advanced.Button(pg.Rect(1150,650,500,200),"Restart",goto,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"functionParameters":[4,"closePopup"]}),
    ],
borderRadius=20)

ppNewGame=pgp.advanced.Popup(rPopup,pgp.Surface.mergeSurface(
                        font2.render("Welcome to Battle Sticks Remastered!",True,"black"),
                        font4.render("This is a Remaster of a game I made a few years ago.",True,"black"),
                        font4.render("The game is pretty hard but you should still try to beat it.",True,"black"),
                        font4.render("The game is both mouse and keyboard.",True,"black"),
                        font4.render("Sadly I still don't have the full hotkey list but coming soon!",True,"black"),
                        font4.render("Keep in mind that this is just a DEMO and I made it in 1 week.",True,"black"),
                        font4.render("Have Fun!",True,"black"),
                        pg.Surface((0,100)),
                        font4.render("                                                                                            -acXelorate",True,"black"),
                        font2.render("",True,"black"),
                        center=False),
buttons=[
    pgp.advanced.Button(pg.Rect(100,650,700,200),"Ok",closePopup,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1}),
    pgp.advanced.Button(pg.Rect(900,650,700,200),"Discord",pgp.advanced.openLink,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"functionParameters":[slDiscord,True]})
    ],
borderRadius=20)

#l=pgp.advanced.Link("Click Me",[100,500],"youtube.com",font1,(100,0,0),(150,0,0),(255,0,0),20)

while run:
    leftclick=0
    rightclick=0
    left=0
    right=0
    up=0
    down=0
    enter=0
    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=0
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE and popup==0:
                goback()
            if event.key==pg.K_F5:
                popup=1
            if event.key==pg.K_F9:
                breakpoint()
            if event.key==pg.K_LEFT:
                left=1
            if event.key==pg.K_RIGHT:
                right=1
            if event.key==pg.K_UP:
                up=1
            if event.key==pg.K_DOWN:
                down=1
            if event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                enter=1
        if event.type==pg.MOUSEBUTTONDOWN:
            if event.button==1:
                leftclick=1
            if event.button==3:
                rightclick=1
        if event.type==pg.MOUSEWHEEL:
            if event.y>0:
                up=1
            if event.y<0:
                down=1
    mousex,mousey=pg.mouse.get_pos()
    mx,my=pgp.point.get_smart_point2(mousex,mousey,cam)
    
    keys=pg.key.get_pressed()
    
    if room in [0,1,2,3]:
        window.fill(Cbackground)
        visual.backgroundEffect()
        visual.drawTitle()
        
    if room in [5,6,7]:
        window.fill(Cbackground)
        visual.backgroundEffect()
        
    if room in [1,2,3]:
        if fLoadout:
            bEquip.step(window,cam,mousex,mousey,leftclick or enter)
        if fShop:
            bShop.step(window,cam,mousex,mousey,leftclick or enter)
    
    if room==0:
        buttonStep(bPlay,popup,window,cam,mousex,mousey,leftclick or enter)
        buttonStep(bCredits,popup,window,cam,mousex,mousey,leftclick or enter)
        buttonStep(bQuit,popup,window,cam,mousex,mousey,leftclick or enter)
        
    elif room==1:
        buttonStep(bCampaign,popup,window,cam,mousex,mousey,leftclick or enter)
        
        
    elif room==2:
        
        if storyTilt==0:
            if up and storyIndex!=0:
                storyIndex-=1
                storyTilt=-400
            
            elif down and storyIndex<len(storyButtons)-1:
                storyIndex+=1
                storyTilt=400
                
        else:
            for button in storyButtons:
                button.Rect.y-=20*pgp.pyplus.getState(storyTilt)
            storyTilt-=20*pgp.pyplus.getState(storyTilt)
        
        for button in storyButtons:
            if button.Rect.y>=250:
                buttonStep(button,popup,window,cam,mousex,mousey,leftclick or enter)
           
    elif room==3:
        
        if levelTilt==0:
            if (left or up) and levelIndex!=0:
                levelIndex-=1
                levelTilt=-700
            
            elif (right or down) and levelIndex<len(levelButtons)-1:
                levelIndex+=1
                levelTilt=700
                
        else:
            for button in levelButtons:
                button.Rect.x-=35*pgp.pyplus.getState(levelTilt)
            levelTilt-=35*pgp.pyplus.getState(levelTilt)
            
        for button in levelButtons:
            buttonStep(button,popup,window,cam,mousex,mousey,leftclick or enter)
            
    elif room==4:
        if popup==0:
            visual.drawInGameBackground()
            mon+=eff
            visual.drawMoney(level,mon)
            visual.drawCastle(hp1,hp2)
            mon=visual.drawPortraits(loadout,mousex,mousey,leftclick,mon,research,keys)
            
            aimon1,aimon2,ai2choice=ai(level,aimon1,aimon2,evils,ai2choice)
            
            for unit in goods:
                hp2,aimon=unit.step(goods,evils,t2,hp2,aimon)
                
            for unit in evils:
                hp1,mon=unit.step(evils,goods,t1,hp1,mon)
                
            if hp2<=0:
                popup=2
                dXp=xp
                
                newShop=0
                if gauntletName=="campaign":
                    gauntlet=campaign
                storyIndex=[i for i,x in enumerate(gauntlet) if level in x["levels"]][0]
                val=[gauntletName,storyIndex,gauntlet[storyIndex]["levels"].index(level)]
                
                if val not in completed:
                    newCompletion=1
                    completed.append(val)
                    if any("limit" in item and item["limit"]==val for item in shop):
                        newShop=True
                    
                    xp+=level["xp"]
                
                else:
                    newCompletion=0
                    if "xp2" in level:
                        xp+=level["xp2"]
                    else:
                        xp+=100
                        
                
                if "unlockFeature" in level:
                    newFeature=False
                    for feature in level["unlockFeature"]:
                        if feature=="loadout":
                            if fLoadout==False:
                                newFeature=True
                                fLoadout=True
                        if feature=="shop":
                            if fShop==False:
                                newFeature=True
                                fShop=True
                
                ppVictoryScreen=pgp.advanced.Popup(
                    rPopup, pgp.Surface.mergeSurface(
                        font2.render("You win!",True,"black"),
                        font2.render(f"+{xp-dXp}xp",True,"black"),
                        font2.render("A new Unit is Unlocked!", True, "black") if "unlockUnit" in level and level["unlockUnit"] not in goodlist else surf,
                        font2.render("A new Feature is Unlocked!", True, "black") if "unlockFeature" in level and newFeature else surf,
                        font2.render("There is something New in the Shop!", True, "black") if newShop else surf,
                        font4.render("Thanks for beating the Battle Sticks Remaster Demo!", True, "black") if newCompletion and val==["campaign",0,20] else surf
                    ),
                    buttons=[
                        pgp.advanced.Button(pg.Rect(510,650,700,200),"Ok",goto,bgColor="gray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"functionParameters":[3,["closePopup","keepIndex"]]})
                    ],
                    borderRadius=20
                )
                if "unlockUnit" in level and level["unlockUnit"] not in goodlist:
                    goodlist.append(level["unlockUnit"])
                    
                if "unlockLevel" in level:
                    if type(level["unlockLevel"][0])==list:
                        for stage in level["unlockLevel"]:
                            if stage not in stages:
                                stages.append(stage)
                    elif level["unlockLevel"] not in stages:
                        stages.append(level["unlockLevel"])
                
                
            if hp1<=0:
                popup=3
                ppLoseScreen=pgp.advanced.Popup(rPopup,
                                                font2.render("You Lose!",True,"black"),
                                                buttons=[
                                                    pgp.advanced.Button(pg.Rect(100,650,700,200),"Ok",goto,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"functionParameters":[3,["closePopup","ignore"]]}),
                                                    pgp.advanced.Button(pg.Rect(900,650,700,200),"Try Again",goto,"lightgray",fontName=sFont1Bold,fontSize=75,hoverEffect="popup",borderRadius=20,flags={"hoverSfx":sSfx1,"functionParameters":[4,"closePopup"]})
                                                    ],
                                                borderRadius=20
                                                )
                
            
    elif room==5:
        equip,unitX,unitTilt,unitIndex=visual.drawLoadout(equip,goodlist,unitX,unitIndex,unitTilt,left,right,enter,keys,mousex,mousey,leftclick,rightclick)
            
    elif room==6:
        visual.drawTitleShop(xp)
        x=shopX
        
        shopSize=-1
        for item in shop:
            if not "limit" in item or "limit" in item and item["limit"] in completed:
                shopSize+=1
        
        if shopTilt!=0:
            shopX-=40*pgp.pyplus.getState(shopTilt)
            shopTilt-=40*pgp.pyplus.getState(shopTilt)
        
        if (right or down) and shopTilt==0 and shopIndex<shopSize:
            shopTilt=400
            shopIndex+=1
            
        if (left or up) and shopTilt==0 and shopIndex!=0:
            shopTilt=-400
            shopIndex-=1
        
        pgp.draw.rect(window,cam,"yellow",pg.Rect(cx-190,135,380,910),5)
        for item in shop:
            if "limit" in item and item["limit"] not in completed:
                continue
            color=shopColor[item["type"]]
            
            pgp.draw.rect(window,cam,color[0],pg.Rect(x,140,370,900))
            pgp.draw.rect(window,cam,color[1],pg.Rect(x,140,370,100))
            pgp.draw.rect(window,cam,color[1],pg.Rect(x,600,370,100))
            
            rect=shopText[item["type"]].get_rect(center=[x+185,190])
            pgp.blit(window,cam,shopText[item["type"]],rect)
            
            if item["type"]=="unit":
                pgp.blit(window,cam,pg.transform.scale(img[item["index"]][1],[360,360]),x+5,240)
                txt=font2.render(stats[item["index"]]["name"],True,"white")
                rect=txt.get_rect(centerx=x+185,y=600)
                pgp.blit(window,cam,txt,rect)
                
                def func():
                    global xp
                    xp-=cost
                    goodlist.append(item["index"])
                    sfx3.play()
                
            if item["type"]=="upgrade":
                txt=font5.render(item["name"],True,"white")
                rect=txt.get_rect(centerx=x+185,y=610)
                pgp.blit(window,cam,txt,rect)
                
                def func():
                    global xp
                    xp-=cost
                    
                    sfx3.play()
                    
                    if item["name"]=="Efficiency":
                        global efficiency
                        efficiency+=1
                
                if item["name"]=="Efficiency":
                    upgrade=efficiency
                
                txt=font6.render(shopUpgradeSprite[upgrade-1],True,"white")
                rect=txt.get_rect(center=[x+185,420])
                pgp.blit(window,cam,txt,rect)
                
            if item["type"]!="upgrade":
                cost=item["cost"]
            else:
                cost=int(item["cost"]/1.2*(upgrade)*1.2)
            if len(str(cost))<5:
                txt=font2.render(f"{cost}xp",True,"white")
            else:
                txt=font5.render(f"{cost}xp",True,"white")
            rect=txt.get_rect(centerx=x+185,centery=735)
            pgp.blit(window,cam,txt,rect)
            
            
            rect=pg.Rect(0,850,300,150)
            rect.centerx=x+185
            
            
            if (item["type"]=="unit" and item["index"] in goodlist) or (item["type"]=="upgrade" and upgrade==item["cap"]):
                b=pgp.advanced.Button(rect,"Sold Out",lambda: None,bgColor="gray",fontName=sFont1Bold,fontSize=60,borderRadius=20)
            else:
                if cost<=xp:
                    b=pgp.advanced.Button(rect,"BUY",func,fontName=sFont1Bold,fontSize=100,borderRadius=20)
                else:
                    b=pgp.advanced.Button(rect,"BUY",lambda: None,bgColor="gray",fontName=sFont1Bold,fontSize=100,borderRadius=20)
            b.step(window,cam,mousex,mousey,leftclick)
            
            pgp.draw.line(window,cam,color[2],[x,240],[x+370,240],5)
            pgp.draw.line(window,cam,color[2],[x,600],[x+370,600],5)
            pgp.draw.line(window,cam,color[2],[x,700],[x+370,700],5)
            pgp.draw.rect(window,cam,color[2],pg.Rect(x,140,370,900),5)
            
            
            x+=400
            
    elif room==7:
        visual.drawTitleCredits()
        
        pgp.blit(window,cam,tCredits1,50,150)
        linkStep(lCredits1,popup,window,cam,mousex,mousey,leftclick)
        linkStep(lCredits2,popup,window,cam,mousex,mousey,leftclick)
            
        pgp.blit(window,cam,tCredits2,50,300)
        linkStep(lCredits3,popup,window,cam,mousex,mousey,leftclick)
        linkStep(lCredits4,popup,window,cam,mousex,mousey,leftclick)
        linkStep(lCredits5,popup,window,cam,mousex,mousey,leftclick)
            
    else:
        window.fill("black")
        pgp.blit(window,cam,tOOB,rtOOB)
        
    if popup==1:
        ppQuit.step(window,cam,mousex,mousey,leftclick)
    if popup==2:
        ppVictoryScreen.step(window,cam,mousex,mousey,leftclick)
    if popup==3:
        ppLoseScreen.step(window,cam,mousex,mousey,leftclick)
    if popup==4:
        ppPause.step(window,cam,mousex,mousey,leftclick)
    if popup==5:
        ppNewGame.step(window,cam,mousex,mousey,leftclick)
    
    pg.display.update()
    clock.tick(60)
saveData()
print("Goodbye")
pg.quit()